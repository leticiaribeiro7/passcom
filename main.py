import requests
from flask import Flask, jsonify, request
from prisma import Prisma, register
import os, json
import uuid

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]





# Endpoint para obter trechos deste servidor
@app.route("/trechos", methods=["GET"])
def get_trechos():
    trechos = db.trecho.find_many()
    return jsonify({
        "data": [trecho.dict() for trecho in trechos]
    })

# Função para obter trechos de outros servidores
def get_trechos_from_other_servers():
    all_trechos = []
    
    for url in urls:
        try:
            response = requests.get(f'{url}/trechos')
            if response.status_code == 200:
                trechos = response.json().get('data', [])
                all_trechos.extend(trechos)
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
    
    return all_trechos

# reserva um trecho 
@app.route("/reservar-trecho", methods=["POST"])
def post_trecho():    
    data = json.loads(request.data)
    db.trechoreservado.create({
        "uuid_passagem": data.get('uuid_passagem'),
        "id_assento": data.get('id_assento'),
        "id_trecho": data.get('id_trecho')
    })

    return jsonify({"message": "Trecho reservado"}), 200

# cria uma passagem, recebe userid e uuid (id unico passagem)
@app.route("/passagem", methods=["POST"])
def post_passagem():
    data = json.loads(request.data)
    db.passagem.create({
        "user_id": data.get('user_id'),
        "uuid": data.get('uuid')
    })

    return jsonify({"message": "Passagem criada com sucesso"}), 200

# busca tds as passagens do user - /passagem/1
@app.route("/passagem/<user_id>", methods=["GET"])
def get_passagem(user_id):
    passagens = db.passagem.find_many(where={"user_id": int(user_id)})
    return jsonify({"data": [passagem.dict() for passagem in passagens]}), 200


@app.route("/passagem/<user_id>/<uuid>", methods=["DELETE"])
def delete_passagem(user_id, uuid):
    try:
        deleted_passagem = db.passagem.delete(
            where = {
                "user_id": int(user_id),
                "uuid": uuid
            }
        )

        if deleted_passagem['count'] == 0:
            return jsonify({"message": "Nenhuma passagem encontrada para deletar"}), 404
        
        return jsonify({"message": "Passagem deletada com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/user", methods=["POST"])
def create_user():
    try:
        data = json.loads(request.data)
        db.user.create({
            "login": data.get('login'),
            "password": data.get('password'),
            "name": data.get('name')
        })
    except Exception as e:
        return jsonify({"error": "Erro ao criar usuário"}), 500

@app.route("/create-user-all", methods=["POST"])
def create_users_all_servers():
    data = json.loads(request.data)
    # cria mesmo user em todos os servers
    for url in urls:
        try:
            response = requests.post(f'{url}/user', json={
                "login": data.get('login'),
                "password": data.get('password'),
                "name": data.get('name')}
            )
            return jsonify({
                "message": "Usuário criado com sucesso"
            })
        
        except Exception as e:
            return jsonify({
                "message": "Erro ao criar usuário"
            }), 500
            

#  obter todos os trechos
@app.route("/all-trechos", methods=["GET"])
def get_all_trechos():
    all_trechos = []
    
    # Adiciona os trechos de todos os servidores
    all_trechos.extend(get_trechos_from_other_servers())
    
    return jsonify({
        "data": all_trechos
    })

# cria uma reserva, recebe userid e lista de trechos
@app.route("/reservar", methods=["POST"])
def reservar_assento():
    data = json.loads(request.data) # lista

    uuid_passagem = str(uuid.uuid4())
    # cria a mesma passagem em todos os servers
    for url in urls:
        try:
            response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_id": int(data['user_id'])})
            print(response.status_code)
        except Exception as e:
            return jsonify({"error": "Erro ao reservar"}), 500
            
    for trecho in data.get('trechos', []):
        
        dados = {
            "id_trecho": int(trecho.get('id_trecho')),
            "id_assento": int(trecho.get('id_assento')),
            "uuid_passagem": uuid_passagem
        }
        # cria os trechos reservados na companhia que pertence
        requests.post(f'http://company_{trecho.get('company')}:5000/reservar-trecho', json=dados)

    return jsonify({
        "message": "Reserva efetuada com sucesso"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')


    