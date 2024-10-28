from db_config import db
from flask import Blueprint, jsonify, request
import requests
import json

users_bp = Blueprint("users", __name__)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]



@users_bp.route("/create-user-all", methods=["POST"])
def create_users_all_servers():
    data = json.loads(request.data)
    # cria mesmo user em todos os servers
    for url in urls:
        try:
            response = requests.post(f'{url}/user', json={
                "login": data.get('login'),
                "password": data.get('password'),
            })
            
            return jsonify({
                "message": "Usuário criado com sucesso"
            })
        
        except Exception as e:
            return jsonify({
                "message": "Erro ao criar usuário"
            }), 500
            