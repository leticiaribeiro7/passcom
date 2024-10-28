from db_config import db
from flask import Blueprint, jsonify, request
import json, requests, os
import uuid
import redis


passagens_bp = Blueprint("passagens", __name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host="redis_host", port=6379, db=0)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]


@passagens_bp.route("/passagem", methods=["POST"])
def post_passagem():
        data = json.loads(request.data)
        db.passagem.create({
            "user_id": data.get('user_id'),
            "uuid": data.get('uuid')
        })

        return jsonify({"message": "Passagem criada com sucesso"}), 200

@passagens_bp.route("/passagem/uuid/<uuid>", methods=["GET"])
def get_passagem_uuid():
    passagem = db.passagem.find_first(where={"uuid": uuid}) #include trechos
    return jsonify({
        "data": passagem.dict()
    })


# busca tds as passagens do user - /passagem/user/1
@passagens_bp.route("/passagem/user/<int:user_id>", methods=["GET"])
def get_passagem_user(user_id):
    passagens = db.passagem.find_many(where={"user_id": int(user_id)}) #include trechos
    return jsonify({"data": [passagem.dict() for passagem in passagens]}), 200



# deleta passagem em tds os servers (cancelamento)
@passagens_bp.route("/passagem-all/<int:user_id>/<uuid>", methods=["DELETE"])
def delete_passagem(user_id, uuid):
    try:
        # pega a passagem com os trechos associados
        passagem = db.passagem.find_unique(
            where={"uuid": uuid},
            include={"trechosreservados": True}  # Inclui os trechos reservados associados à passagem
        )

        if not passagem:
            return jsonify({"message": "Nenhuma passagem encontrada para deletar"}), 404

        # Envia a requisição de cancelamento para os trechos correspondentes nas companhias corretas
        for trecho in passagem.trechos_reservados:

            try:
                requests.delete(f"http://company_{trecho['company']}:5000/trechos-reservados/{uuid}")
            except Exception as e:
                print(f"Erro ao cancelar trecho na companhia {trecho['company']}: {e}")

        
        for url in urls:
            request.delete(f"{url}/passagem/{user_id}/{uuid}")


        return jsonify({"message": "Passagem deletada com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@passagens_bp.route("/passagem/<int:user_id>/<uuid>", methods=["DELETE"])
def delete_pass(user_id, uuid):
    db.passagem.delete(
    where= {
        "user_id": int(user_id),
        "uuid": uuid
    }
)
    
# cria uma reserva, recebe userid e lista de trechos
@passagens_bp.route("/reservar", methods=["POST"])
def reservar_assento():
    data = json.loads(request.data) # lista

    uuid_passagem = str(uuid.uuid4())
    

    #verifica se o assento escolhido ta disponivel em tds os trechos
    for trecho in data.get('trechos', []):
        lock_key = f"trecho_{trecho.get('id_trecho')}_assento_{trecho.get('numero_assento')}"

        lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=30)

        if not lock_acquired:
            return jsonify({"message": "Outro cliente está reservando este assento, tente novamente"}), 409

        try:
            response = requests.get(f'http://company_{trecho.get('company')}:5000/assentos/{trecho.get('id_assento')}')
            assento = response.json().get('data')
            if assento.get('disponivel') == 0:
                return jsonify({"message": "Assento escolhido não está disponível"})
                
        finally:
            redis_client.delete(lock_key)     

    # cria a mesma passagem em todos os servers
    for url in urls:
        try:
            response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_id": int(data['user_id'])})
            print(response.status_code)
        except Exception as e:
            return jsonify({"error": "Erro ao reservar"}), 500
        

    for trecho in data.get('trechos', []):
        
        lock_key = f"trecho_{trecho.gey('id_trecho')}_assento_{trecho.get('numero_assento')}"

        lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=30)

        if not lock_acquired:
            return jsonify({"message": "Outro cliente está reservando este assento, tente novamente"}), 409
        
        try:
            dados = {
                "id_trecho": int(trecho.get('id_trecho')),
                "id_assento": int(trecho.get('id_assento')),
                "uuid_passagem": uuid_passagem
            }

            # cria os trechos reservados na companhia que pertence e bloqueia o assento
            requests.post(f'http://company_{trecho.get('company')}:5000/trecho-reservado', json=dados)
            requests.put(f'http://company_{trecho.get('company')}:5000/assentos/{dados['id_assento']}', json={"disponivel": 0})
        finally:
            # Libera o lock após a reserva e atualização do assento
            redis_client.delete(lock_key)

    return jsonify({
        "message": "Reserva efetuada com sucesso"
    })