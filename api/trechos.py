from db_config import db
from flask import Blueprint, jsonify, request
import requests
from flask_jwt_extended import jwt_required

trechos_bp = Blueprint("trechos", __name__)


urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]


@trechos_bp.route("/trechos", methods=["GET"])
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

@trechos_bp.route("/all-trechos", methods=["GET"])
@jwt_required()
def get_all_trechos():
    all_trechos = []
    
    # Adiciona os trechos de todos os servidores
    all_trechos.extend(get_trechos_from_other_servers())
    
    return jsonify({
        "data": all_trechos
    })