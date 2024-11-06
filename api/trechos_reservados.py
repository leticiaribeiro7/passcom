from db_config import db
from flask import Blueprint, jsonify, request
import json, requests

trechos_reservados_bp = Blueprint("trechos_reservados", __name__)


@trechos_reservados_bp.route("/trecho-reservado", methods=["POST"])
def post_trecho():    
    data = json.loads(request.data)
    db.trechoreservado.create({
        "uuid_passagem": data.get('uuid_passagem'),
        "id_assento": data.get('id_assento'),
        "id_trecho": data.get('id_trecho')
    })

    return jsonify({"message": "Trecho reservado"}), 200


@trechos_reservados_bp.route("/trechos-reservados/<uuid_passagem>", methods=["DELETE"])
def delete_trecho(uuid_passagem):
    try:
        deleted_trechos = db.trechoreservado.delete_many(
            where = {
                "uuid_passagem": uuid_passagem
            }
        )

        if deleted_trechos['count'] == 0:
            return jsonify({"message": "Nenhum trecho encontrado para cancelar"}), 404
        
        return jsonify({"message": "Trechos cancelados com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

