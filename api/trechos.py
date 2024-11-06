from db_config import db
from flask import Blueprint, jsonify, request
import requests
from flask_jwt_extended import jwt_required
import json, os

from utils import urls

trechos_bp = Blueprint("trechos", __name__)

company = os.getenv("COMPANY_NAME") 

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


rotas_unicas = set()


def buscar_rotas_iterativa(origem, destino, trechos):
    rotas_unicas = set()  
    pilha = [(origem, [])]  
    
    while pilha:
        local_atual, rota_atual = pilha.pop()
        
        if local_atual == destino:
            rota_tuple = tuple((trecho['origem'], trecho['destino'], trecho['company'], trecho['id']) for trecho in rota_atual)
            rotas_unicas.add(rota_tuple)
            continue

        for trecho in trechos:
            if trecho['origem'] == local_atual:
                nova_rota = rota_atual + [trecho]
                pilha.append((trecho['destino'], nova_rota))
    
    rotas_formatadas = []
    for rota in rotas_unicas:
        rota_formatada = [
            {
                "origem": trecho[0],
                "destino": trecho[1],
                "company": trecho[2],
                "id_trecho": trecho[3],
                "assentos": [
                    {"id": assento['id'], "numero": assento['numero']}
                    for assento in trecho_data['assentos']
                    if assento['disponivel'] == 1
                ]
            }
            for trecho in rota
            for trecho_data in trechos
            if trecho_data['origem'] == trecho[0] and trecho_data['destino'] == trecho[1] and trecho_data['company'] == trecho[2]
        ]
        rotas_formatadas.append(rota_formatada)

    rotas_final = [trecho for rota in rotas_formatadas for trecho in rota]

    return rotas_final


@trechos_bp.route('/rotas', methods=['POST'])
def rotas():
    data = json.loads(request.data)
    origem = data.get('origem')
    destino = data.get('destino')

    if not origem or not destino:
        return jsonify({"error": "Origem e destino são obrigatórios"}), 400

    todos_trechos = requests.get(f'http://company_{company}:5000/all-trechos').json()
    
    rotas_formatadas = buscar_rotas_iterativa(origem, destino, todos_trechos)

    print(rotas_formatadas)

    return jsonify(rotas_formatadas)