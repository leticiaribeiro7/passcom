from db_config import db
from flask import Blueprint, jsonify, request
import json, requests, os
import uuid
import redis


passagens_bp = Blueprint("passagens", __name__)

redis_host = os.getenv("REDIS_HOST")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]


@passagens_bp.route("/passagem", methods=["POST"])
def post_passagem():
    data = json.loads(request.data)
    db.passagem.create({
        "user_uuid": data.get('user_uuid'),
        "uuid": data.get('uuid')
    })

    return jsonify({"message": "Passagem criada com sucesso"}), 200

@passagens_bp.route("/passagem/uuid/<uuid>", methods=["GET"])
def get_passagem_uuid(uuid):
    passagem = db.passagem.find_first(
        where={"uuid": uuid},
        include={"trechosReservados": True}
    ) #include trechos

    return jsonify({
        "data": passagem.dict()
    })


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
    return jsonify({"data": [passagem.dict() for passagem in passagens]}), 200


@passagens_bp.route("/passagens-all/<user_uuid>", methods=["GET"])
def get_passagem_all_servers(user_uuid):
    passagens_agrupadas = {}

    # Itera sobre cada servidor para buscar as passagens e seus trechos do usuário
    for url in urls:
        try:
            # Solicita todas as passagens do usuário no servidor atual
            response = requests.get(f"{url}/passagem/user/{user_uuid}")
            if response.status_code == 200:
                passagens_data = response.json().get("data", [])

                # Agrupa os trechos por UUID de passagem
                for passagem in passagens_data:
                    uuid_passagem = passagem["uuid"]
                    
                    # Se o UUID da passagem já existe, adiciona apenas os novos trechos
                    if uuid_passagem in passagens_agrupadas:
                        passagens_agrupadas[uuid_passagem]["trechosReservados"].extend(passagem["trechosReservados"])
                    else:
                        # Caso contrário, cria uma nova entrada para a passagem e seus trechos
                        passagens_agrupadas[uuid_passagem] = passagem

        except Exception as e:
            print(f"Erro ao buscar passagens no servidor {url}: {e}")

    # Converte o dicionário de passagens agrupadas em uma lista para resposta
    todas_passagens = list(passagens_agrupadas.values())
    
    # Retorna a lista consolidada de todas as passagens com seus trechos reservados
    if todas_passagens:
        return jsonify({"passagens": todas_passagens}), 200
    else:
        return jsonify({"message": "Nenhuma passagem encontrada para o UUID do usuário fornecido"}), 404


# deleta passagem em tds os servers (cancelamento)
@passagens_bp.route("/passagem-all/<user_uuid>/<uuid>", methods=["DELETE"])
def delete_passagem(user_uuid, uuid):
    try:
        # pega a passagem com os trechos associados
        passagem = db.passagem.find_unique(
            where={"uuid": uuid},
            include={"trechosreservados": True} 
        )

        if not passagem:
            return jsonify({"message": "Nenhuma passagem encontrada para deletar"}), 404

        # Envia a requisição de cancelamento para os trechos correspondentes nas companhias corretas
        for trecho in passagem.trechos_reservados:

            try:
                requests.delete(f"http://company_{trecho['company']}:5000/trechos-reservados/{uuid}")
                requests.put(f"http://company_{trecho['company']}:5000/assentos/{trecho['id']}", json={"disponivel": 1})
            except Exception as e:
                print(f"Erro ao cancelar trecho na companhia {trecho['company']}: {e}")

        
        for url in urls:
            request.delete(f"{url}/passagem/{user_uuid}/{uuid}")


        return jsonify({"message": "Passagem deletada com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@passagens_bp.route("/passagem/<user_uuid>/<uuid>", methods=["DELETE"])
def delete_pass(user_uuid, uuid):
    db.passagem.delete(
    where= {
        "user_uuid": user_uuid,
        "uuid": uuid
    }
)


# aux
def check_disponibilidade(trecho):
    lock_key = f"company_{trecho.get('company')}_trecho_{trecho.get('id_trecho')}_assento_{trecho.get('numero_assento')}"
    lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=30)

    if not lock_acquired:
        return False, {"message": "Outro cliente está reservando este assento, tente novamente"}, 409

    try:
        # Verifica se o assento ta disponível
        response = requests.get(f'http://company_{trecho.get("company")}:5000/assentos/{trecho.get("id_assento")}')
        assento = response.json().get('data')

        if assento.get('disponivel') == 0:
            redis_client.delete(lock_key)  # Libera o lock se não estiver disponível
            return False, {"message": "Assento não está disponível"}, 409

    except Exception:
        redis_client.delete(lock_key)  # Libera o lock no caso de erro
        return False, {"message": "Erro ao verificar assento"}, 500

    return True, lock_key
    
# cria uma reserva, recebe userid e lista de trechos
@passagens_bp.route("/reservar", methods=["POST"])
def reservar_assento():
    data = json.loads(request.data)
    uuid_passagem = str(uuid.uuid4())
    locked_keys = []  # Lista de locks para liberar no final

    # verifica disponibilidade e bloqueia todos os assentos
    for trecho in data.get('trechos', []):
        success, result = check_disponibilidade(trecho)

        if not success:
            # Se o assento do trecho não estiver disponível, libera locks
            for key in locked_keys:
                redis_client.delete(key)
            return jsonify(result), result[1]  # Retorna mensagem de erro e codigo de erro

        locked_keys.append(result)

    # Cria a passagem em todos os servidores
    for url in urls:
        try:
            response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_uuid": data['user_uuid']})
            print(response.status_code)
        except Exception:
            for key in locked_keys:
                redis_client.delete(key)
            return jsonify({"error": "Erro ao criar a passagem"}), 500

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