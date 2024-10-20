import requests
from flask import Flask, jsonify
from prisma import Prisma, register
import os 

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

# Endpoint para obter trechos deste servidor
@app.route("/trechos", methods=["GET"])
def get_trechos():
    trechos = db.trecho.find_many()
    return jsonify({
        "data": [trecho.dict() for trecho in trechos]
    })

# Função para obter trechos de outros servidores
def get_trechos_from_other_servers():
    urls = [
        "http://company_a:5000",
        "http://company_b:5000",
        "http://company_c:5000"
    ]
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

# Endpoint para obter todos os trechos (de todos os servidores)
@app.route("/all-trechos", methods=["GET"])
def get_all_trechos():
    all_trechos = []
    
    # Adiciona os trechos de todos os servidores
    all_trechos.extend(get_trechos_from_other_servers())
    
    return jsonify({
        "data": all_trechos
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')


