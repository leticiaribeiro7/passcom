from db_config import db
from flask import Blueprint, jsonify, request
import json, requests

assentos_bp = Blueprint("assentos", __name__)


#busca assentos relacionados ao trecho
@assentos_bp.route("/trechos/<int:id_trecho>/assentos", methods=["GET"])
def get_assentos(id_trecho):
    assentos = db.assento.find_many(where={"id_trecho": id_trecho})
    return jsonify({
        "data": [assento.dict() for assento in assentos]
    })

# atualiza assento pra disponivel ou não quando reservar/cancelar atraves do id do assento
@assentos_bp.route("/assentos/<int:id>", methods=["PUT", "GET"])
def put_assentos(id):
    if request.method == "PUT":
        data = json.loads(request.data)
        db.assento.update(
            where={
                "id": id
            },
            data={"disponivel": data.get('disponivel')}
        )
        return jsonify({"message": "Assento atualizado"})
    
    elif request.method == "GET":
        assento = db.assento.find_unique(where={"id": id})

        return jsonify({
            "data": assento.dict()
        })


