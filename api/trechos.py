from db_config import db
from flask import Blueprint, jsonify, request
import requests
from flask_jwt_extended import jwt_required

from utils import urls

trechos_bp = Blueprint("trechos", __name__)


@trechos_bp.route("/trechos", methods=["GET"])
def get_trechos():
    trechos = db.trecho.find_many(include={"assentos": True})
    data = [
        {
            "id": trecho.id,
            "company": trecho.company,
            "origem": trecho.origem,
            "destino": trecho.destino,
            "assentos": [
                {
                    "id": assento.id,
                    "numero": assento.numero,
                    "disponivel": assento.disponivel
                }
                for assento in trecho.assentos if assento.disponivel == 1
            ]
        }
        for trecho in trechos
    ]

    return jsonify(data)


@trechos_bp.route("/all-trechos", methods=["GET"])
@jwt_required()
def get_all_trechos():
    all_trechos = []
    
    for url in urls:
        try:
            response = requests.get(f'{url}/trechos')
            if response.status_code == 200:
                trechos = response.json()
                all_trechos.extend(trechos)
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

    
    return jsonify(all_trechos)