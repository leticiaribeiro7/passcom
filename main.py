import requests
from flask import Flask, jsonify, request
from prisma import Prisma, register
import os, json
import uuid

from db_config import db
from api.assentos import assentos_bp
from api.passagens import passagens_bp
from api.trechos import trechos_bp
from api.users import users_bp
from api.trechos_reservados import trechos_reservados_bp

from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'chave-aqui'
jwt = JWTManager(app)

db.connect()
app.register_blueprint(assentos_bp)
app.register_blueprint(passagens_bp)
app.register_blueprint(trechos_bp)
app.register_blueprint(users_bp)
app.register_blueprint(trechos_reservados_bp)

urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]



# # Endpoint para obter trechos deste servidor
# @app.route("/trechos", methods=["GET"])
# def get_trechos():
#     trechos = db.trecho.find_many()
#     return jsonify({
#         "data": [trecho.dict() for trecho in trechos]
#     })
# # atualiza assento pra disponivel ou não quando reservar/cancelar atraves do id do assento
# @app.route("/assentos/<int:id>", methods=["PUT", "GET"])
# def put_assentos(id):
#     if request.method == "PUT":
#         data = json.loads(request.data)
#         db.assento.update(
#             where={
#                 "id_assento": id
#             },
#             data={"disponivel": data.get('disponivel')}
#         )
#         return jsonify({"message": "Assento atualizado"})
    
#     elif request.method == "GET":
#         assento = db.assento.find_unique(where={"id": id})

#         return jsonify({
#             "data": assento.dict()
#         })

# #busca assentos relacionados ao trecho
# @app.route("/trechos/<int:id_trecho>/assentos", methods=["GET"])
# def get_assentos(id_trecho):
#     assentos = db.assento.find_many(where={"id_trecho": id_trecho})
#     return jsonify({
#         "data": [assento.dict() for assento in assentos]
#     })

# # Função para obter trechos de outros servidores
# def get_trechos_from_other_servers():
#     all_trechos = []
    
#     for url in urls:
#         try:
#             response = requests.get(f'{url}/trechos')
#             if response.status_code == 200:
#                 trechos = response.json().get('data', [])
#                 all_trechos.extend(trechos)
#         except Exception as e:
#             print(f"Erro ao acessar {url}: {e}")
    
#     return all_trechos

# # reserva um trecho 
# @app.route("/trecho-reservado", methods=["POST"])
# def post_trecho():    
#     data = json.loads(request.data)
#     db.trechoreservado.create({
#         "uuid_passagem": data.get('uuid_passagem'),
#         "id_assento": data.get('id_assento'),
#         "id_trecho": data.get('id_trecho')
#     })

#     return jsonify({"message": "Trecho reservado"}), 200

# @app.route("/trechos-reservados/<uuid_passagem>", methods=["DELETE"])
# def delete_trecho(uuid_passagem):
#     try:
#         deleted_trechos = db.trechoreservado.delete_many(
#             where = {
#                 "uuid_passagem": uuid_passagem
#             }
#         )

#         if deleted_trechos['count'] == 0:
#             return jsonify({"message": "Nenhum trecho encontrado para cancelar"}), 404
        
#         return jsonify({"message": "Trecho cancelado com sucesso"}), 200
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # cria uma passagem, recebe userid e uuid (id unico passagem)
# @app.route("/passagem", methods=["POST"])
# def post_passagem():
#         data = json.loads(request.data)
#         db.passagem.create({
#             "user_id": data.get('user_id'),
#             "uuid": data.get('uuid')
#         })

#         return jsonify({"message": "Passagem criada com sucesso"}), 200

# @app.route("/passagem/uuid/<uuid>", methods=["GET"])
# def get_passagem_uuid():
#     passagem = db.passagem.find_first(where={"uuid": uuid}) #include trechos
#     return jsonify({
#         "data": passagem.dict()
#     })


# # busca tds as passagens do user - /passagem/1
# @app.route("/passagem/user/<int:user_id>", methods=["GET"])
# def get_passagem_user(user_id):
#     passagens = db.passagem.find_many(where={"user_id": int(user_id)}) #include trechos
#     return jsonify({"data": [passagem.dict() for passagem in passagens]}), 200



# # deleta passagem em tds os servers
# @app.route("/passagem-all/<int:user_id>/<uuid>", methods=["DELETE"])
# def delete_passagem(user_id, uuid):
#     try:
#         # pega a passagem com os trechos associados
#         passagem = db.passagem.find_unique(
#             where={"uuid": uuid},
#             include={"trechosreservados": True}  # Inclui os trechos reservados associados à passagem
#         )

#         if not passagem:
#             return jsonify({"message": "Nenhuma passagem encontrada para deletar"}), 404

#         # Envia a requisição de cancelamento para os trechos correspondentes nas companhias corretas
#         for trecho in passagem.trechos_reservados:

#             try:
#                 requests.delete(f"http://company_{trecho['company']}:5000/trechos-reservados/{uuid}")
#             except Exception as e:
#                 print(f"Erro ao cancelar trecho na companhia {trecho['company']}: {e}")

        
#         for url in urls:
#             request.delete(f"{url}/passagem/{user_id}/{uuid}")


#         return jsonify({"message": "Passagem deletada com sucesso"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/passagem/<int:user_id>/<uuid>", methods=["DELETE"])
# def delete_pass(user_id, uuid):
#     db.passagem.delete(
#     where= {
#         "user_id": int(user_id),
#         "uuid": uuid
#     }
# )


# @app.route("/user", methods=["POST"])
# def create_user():
#     try:
#         data = json.loads(request.data)
#         db.user.create({
#             "login": data.get('login'),
#             "password": data.get('password'),
#         })
#     except Exception as e:
#         return jsonify({"error": "Erro ao criar usuário"}), 500


# @app.route("/create-user-all", methods=["POST"])
# def create_users_all_servers():
#     data = json.loads(request.data)
#     # cria mesmo user em todos os servers
#     for url in urls:
#         try:
#             response = requests.post(f'{url}/user', json={
#                 "login": data.get('login'),
#                 "password": data.get('password'),
#             })
            
#             return jsonify({
#                 "message": "Usuário criado com sucesso"
#             })
        
#         except Exception as e:
#             return jsonify({
#                 "message": "Erro ao criar usuário"
#             }), 500
            

# #  obter todos os trechos
# @app.route("/all-trechos", methods=["GET"])
# def get_all_trechos():
#     all_trechos = []
    
#     # Adiciona os trechos de todos os servidores
#     all_trechos.extend(get_trechos_from_other_servers())
    
#     return jsonify({
#         "data": all_trechos
#     })

# # cria uma reserva, recebe userid e lista de trechos
# @app.route("/reservar", methods=["POST"])
# def reservar_assento():
#     data = json.loads(request.data) # lista

#     uuid_passagem = str(uuid.uuid4())
#     #verifica se o assento escolhido ta disponivel em tds os trechos
#     for trecho in data.get('trechos', []):
#         response = requests.get(f'http://company_{trecho.get('company')}:5000/assentos/{trecho.get('id_assento')}')
#         assento = response.json().get('data')
#         if assento.get('disponivel') == 0:
#             return jsonify({"message": "Assento escolhido não está disponível"})
                
                

#     # cria a mesma passagem em todos os servers
#     for url in urls:
#         try:
#             response = requests.post(f'{url}/passagem', json={"uuid": uuid_passagem, "user_id": int(data['user_id'])})
#             print(response.status_code)
#         except Exception as e:
#             return jsonify({"error": "Erro ao reservar"}), 500
        

#     for trecho in data.get('trechos', []):
        
#         dados = {
#             "id_trecho": int(trecho.get('id_trecho')),
#             "id_assento": int(trecho.get('id_assento')),
#             "uuid_passagem": uuid_passagem
#         }

#         # cria os trechos reservados na companhia que pertence e bloqueia o assento
#         requests.post(f'http://company_{trecho.get('company')}:5000/trecho-reservado', json=dados)
#         requests.put(f'http://company_{trecho.get('company')}:5000/assentos/{dados['id_assento']}', json={"disponivel": 0})

#     return jsonify({
#         "message": "Reserva efetuada com sucesso"
#     })


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')


    