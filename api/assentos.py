from db_config import db
from flask import Blueprint, jsonify, request
import json

assentos_bp = Blueprint("assentos", __name__)

# Atualiza assento pra disponivel ou não disponível quando reservar ou cancelar passagem
# Busca o assento pelo id para saber se está disponível
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

        return assento.dict()


