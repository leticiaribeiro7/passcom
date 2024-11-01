from db_config import db
from flask import Blueprint, jsonify, request
import requests
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import uuid

users_bp = Blueprint("users", __name__)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]



def get_user(login, password):
    return db.user.find_first(where={"login": login, "password": password})
    


@users_bp.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    login = data.get('login')
    password = data.get('password')

    if get_user(login, password):
        access_token = create_access_token(identity=login)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas"}), 401


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
        
            if response.status_code == 200:
                responses.append(response.json())

        except Exception as e:
            print(f'Erro no servidor {url}')

    if responses:
        return responses
    else:
        return {"error": "Falha em todos os servidores"}