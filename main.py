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


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')


    