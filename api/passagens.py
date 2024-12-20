from db_config import db
from flask import Blueprint, jsonify, request
import json, requests, os
import uuid
import redis
from flask_jwt_extended import jwt_required

from utils import check_disponibilidade, urls


passagens_bp = Blueprint("passagens", __name__)

redis_host = os.getenv("REDIS_HOST")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@passagens_bp.route("/passagem", methods=["POST"])
def post_passagem():
    data = json.loads(request.data)
    db.passagem.create({
        "user_uuid": data.get('user_uuid'),
        "uuid": data.get('uuid')
    })

    return jsonify({"message": "Passagem criada com sucesso"}), 200


# busca tds as passagens do user (atraves do uuid dele)
@passagens_bp.route("/passagem/user/<user_uuid>", methods=["GET"])
def get_passagem_user(user_uuid):
    passagens = db.passagem.find_many(
        where={
            "user_uuid": user_uuid
        }, 
        include={
            "trechosReservados": {
                "include": {
                    "trecho": True,
                    "assento": True
                }
            }
        })
    
    passagens_simplificadas = [
        {
            "uuid": passagem.uuid,
            "created_at": passagem.created_at,
            "trechosReservados": [
                {
                    "trecho": {
                        "origem": trecho_reservado.trecho.origem,
                        "destino": trecho_reservado.trecho.destino,
                        "company": trecho_reservado.trecho.company
                    },
                    "assento": {
                        "numero": trecho_reservado.assento.numero,
                        "disponivel": trecho_reservado.assento.disponivel
                    }
                }
                for trecho_reservado in passagem.trechosReservados
            ]
        }
        for passagem in passagens
    ]

    return jsonify(passagens_simplificadas), 200


@passagens_bp.route("/passagens-all/<user_uuid>", methods=["GET"])
@jwt_required()
def get_passagem_all_servers(user_uuid):
    passagens_agrupadas = {}

    # Itera sobre cada servidor para buscar as passagens e seus trechos do usuário
    for url in urls:
        try:
            # Solicita todas as passagens do usuário no servidor atual
            response = requests.get(f"{url}/passagem/user/{user_uuid}", timeout=10)
            if response.status_code == 200:
                passagens_data = response.json()

                # Agrupa os trechos por UUID de passagem
                for passagem in passagens_data:
                    uuid_passagem = passagem["uuid"]
                    
                    # Se o UUID da passagem já existe, adiciona apenas os novos trechos
                    if uuid_passagem in passagens_agrupadas:
                        passagens_agrupadas[uuid_passagem]["trechosReservados"].extend(passagem["trechosReservados"])
                    else:
                        # Caso contrário, cria uma nova entrada para a passagem e seus trechos
                        passagens_agrupadas[uuid_passagem] = {
                            "uuid": passagem["uuid"],
                            "created_at": passagem["created_at"],
                            "trechosReservados": passagem["trechosReservados"]
                        }

        except Exception as e:
            print(f"Erro ao buscar passagem no servidor {url}, {e}")

    todas_passagens = list(passagens_agrupadas.values())
    
    if todas_passagens:
        return jsonify(todas_passagens), 200
    else:
        return jsonify({"message": "Nenhuma passagem encontrada para o UUID do usuário fornecido"}), 404


# deleta passagem em tds os servers (cancelamento)
@passagens_bp.route("/passagem-all/<user_uuid>/<uuid>", methods=["DELETE"])
@jwt_required()
def delete_passagem(user_uuid, uuid):
    try:
        # pega a passagem com os trechos associados
        passagem = db.passagem.find_unique(
            where={"uuid": uuid},
            include={
            "trechosReservados": {
                "include": {
                    "trecho": True,
                    "assento": True
                }
            }
        })

        if not passagem:
            return jsonify({"message": "Nenhuma passagem encontrada para deletar"}), 404
        

        # Deleta os trechos reservados de cada companhia e libera assentos
        for trechoReservado in passagem.trechosReservados:

            try:
                requests.delete(f"http://company_{trechoReservado.trecho.company}:5000/trechos-reservados/{uuid}")
                requests.put(f"http://company_{trechoReservado.trecho.company}:5000/assentos/{trechoReservado.assento.numero}", json={"disponivel": 1})
            except Exception as e:
               return jsonify({"error": str(e)}), 500

        
        for url in urls:
            response = requests.delete(f"{url}/passagem/{user_uuid}/{uuid}")


        return response.json()

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@passagens_bp.route("/passagem/<user_uuid>/<uuid>", methods=["DELETE"])
def delete_pass(user_uuid, uuid):
    db.passagem.delete(
    where= {
        "user_uuid": user_uuid,
        "uuid": uuid
    })

    return jsonify({"message": "Passagem deletada com sucesso"}), 200

    
# cria uma reserva, recebe userid e lista de trechos
@passagens_bp.route("/reservar", methods=["POST"])
@jwt_required()
def reservar_assento():
    
    if not request.is_json:
        return jsonify({"error": "Requisição deve conter um JSON válido"}), 400


    data = json.loads(request.data)
    uuid_passagem = str(uuid.uuid4())
    locked_keys = []  # lista de locks para liberar no final

    # verifica disponibilidade e bloqueia todos os assentos
    for trecho in data.get('trechos', []):
        success, result, status_code = check_disponibilidade(trecho, redis_client)

        if not success:
            # Se o assento do trecho não estiver disponível, libera locks
            for key in locked_keys:
                redis_client.delete(key)
            return jsonify(result), status_code  # Retorna mensagem de erro e codigo de erro

        locked_keys.append(result)

    # Cria a passagem em todos os servidores
    for url in urls:
        try:
            response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_uuid": data['user_uuid']})
            print(response.status_code)
        except Exception:
            print("Erro ao criar a passagem no servidor {url}")

    # reserva os trechos após criar a passagem, so depois libera os locks
    for trecho, lock_key in zip(data.get('trechos', []), locked_keys):
        try:
            dados = {
                "id_trecho": int(trecho.get('id_trecho')),
                "id_assento": int(trecho.get('id_assento')),
                "uuid_passagem": uuid_passagem
            }
            # Cria o trecho reservado e atualiza o status do assento
            requests.post(f'http://company_{trecho.get("company")}:5000/trecho-reservado', json=dados)
            requests.put(f'http://company_{trecho.get("company")}:5000/assentos/{dados["id_assento"]}', json={"disponivel": 0})
        finally:
            redis_client.delete(lock_key)  # Libera o lock após a reserva

    return jsonify({"message": "Reserva efetuada com sucesso"})