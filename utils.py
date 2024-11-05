import os, requests
from db_config import db


urls = [
    "http://company_a:5000",
    "http://company_b:5000",
    "http://company_c:5000"
]


def check_disponibilidade(trecho, redis_client):
    lock_key = f"company_{trecho.get('company')}_trecho_{trecho.get('id_trecho')}_assento_{trecho.get('numero_assento')}"
    lock_acquired = redis_client.set(lock_key, "locked", nx=True, ex=30)

    if not lock_acquired:
        return False, {"message": "Outro cliente está reservando este assento, tente novamente"}, 409

    try:
        # Verifica se o assento ta disponível
        response = requests.get(f'http://company_{trecho.get("company")}:5000/assentos/{trecho.get("id_assento")}')
        assento = response.json()

        if assento.get('disponivel') == 0:
            redis_client.delete(lock_key)  # Libera o lock se não estiver disponível
            return False, {"message": "Assento não está disponível"}, 409

    except Exception:
        redis_client.delete(lock_key)  # Libera o lock no caso de erro
        return False, {"message": "Erro ao verificar assento"}, 500

    return True, lock_key, 200
    


def get_user(login, password):
    return db.user.find_first(where={"login": login, "password": password})
    

