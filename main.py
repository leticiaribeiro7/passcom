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


@app.route("/reservar-trecho", method=["POST"])
def post_trecho():    
    data = json.loads(request.data)
    db.trechoreservado.create({
        "uuid_passagem": data.get('uuid_passagem'),
        "id_assento": data.get('id_assento'),
        "id_trecho": data.get('id_trecho')
    })

    return jsonify({"message": "Trecho reservado"}), 200


@app.route("/passagem", method=["POST"])
def post_passagem():
    data = json.loads(request.data)
    db.passagem.create({
        "user_id": data.get('user_id')
    })

    return jsonify({"message": "Passagem criada com sucesso"}), 200


#  obter todos os trechos
@app.route("/all-trechos", methods=["GET"])
def get_all_trechos():
    all_trechos = []
    
    # Adiciona os trechos de todos os servidores
    all_trechos.extend(get_trechos_from_other_servers())
    
    return jsonify({
        "data": all_trechos
    })
@app.route("/reservar", methods=["POST"])
def reservar_assento():
    data = json.loads(request.data) # lista

    uuid_passagem = str(uuid.uuid4())
   
    for url in urls:
        response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_id": data['user_id']})

    for trecho in data:
        
        dados = {
            "id_trecho": int(trecho.get('id_trecho')),
            "id_assento": int(trecho.get('id_assento')),
            "uuid_passagem": uuid_passagem
        }

        if trecho.get('company') == 1:
            requests.post('http://company_a:5000/reservar-trecho', json=dados)
        elif trecho.get('company') == 2:
            requests.post('http://company_b:5000/reservar-trecho', json=dados)
        elif trecho.get('company') == 3:
            requests.post('http://company_c:5000/reservar-trecho', json=dados) 

    return jsonify({
        "message": "Reserva efetuada com sucesso"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')


    