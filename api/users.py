from db_config import db
from flask import Blueprint, jsonify, request
import requests
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import uuid

from utils import urls, get_user

users_bp = Blueprint("users", __name__)



@users_bp.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    login = data.get('login')
    password = data.get('password')

    user = get_user(login, password)
    if user:
        access_token = create_access_token(identity=login)

        return jsonify(access_token=access_token, user_uuid=user.uuid), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401


@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = json.loads(request.data)

        db.user.create({
            "login": data.get('login'),
            "password": data.get('password'),
            "uuid": data.get('uuid')
        })
        return jsonify({"message": "Usuário criado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao criar usuário"}), 500

@users_bp.route("/register-all", methods=["POST"])
def create_users_all_servers():
    
    if not request.is_json:
        return jsonify({"error": "Requisição deve conter um JSON válido"}), 400
    data = json.loads(request.data)
    uuid_user = str(uuid.uuid4())
    responses = []
    
    # cria mesmo user em todos os servers
    for url in urls:
        try:
            response = requests.post(f'{url}/register', json={
                "uuid": uuid_user,
                "login": data.get('login'),
                "password": data.get('password'),
            }, timeout=10)

        except Exception as e:
            print(f'Erro no servidor {url}')

    return response.json()