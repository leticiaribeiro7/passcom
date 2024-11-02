import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# URLs de login e reserva dos três servidores
login_urls = [
    "http://localhost:5000/login",  # Servidor A
    "http://localhost:5001/login",  # Servidor B
    "http://localhost:5002/login"   # Servidor C
]
server_urls = [
    "http://localhost:5000/reservar",  # Servidor A
    "http://localhost:5001/reservar",  # Servidor B
    "http://localhost:5002/reservar"   # Servidor C
]

# Credenciais para login
credentials = {"login": "usuario_shared_2", "password": "senha2"}

# Dados da reserva (simulação)
reserva_data = {
    "user_uuid": "uuid2",
    "trechos": [
        {
            "id_trecho": 1,
            "id_assento": 5,
            "company": "a"
        }
    ]
}

# Função para fazer login e obter o token JWT
def get_jwt_token(login_url):
    try:
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Erro no login de {login_url}: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Erro ao conectar em {login_url}: {e}")
        return None

# Função para fazer requisição de reserva com o token JWT
def make_reservation(url, token, reserva_data):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, json=reserva_data, headers=headers)
        return {"status_code": response.status_code, "data": response.json(), "url": url}
    except requests.RequestException as e:
        return {"error": str(e), "url": url}

# Configuração de requisições simultâneas
num_requests = 30

# Obtenção dos tokens para cada servidor
tokens = [get_jwt_token(url) for url in login_urls]

# Executor para gerenciar threads
with ThreadPoolExecutor(max_workers=num_requests * len(server_urls)) as executor:
    # Cria uma lista de futuras chamadas para fazer reservas em cada servidor com seus respectivos tokens
    futures = [
        executor.submit(make_reservation, url, tokens[i], reserva_data)
        for i, url in enumerate(server_urls)
        for _ in range(num_requests)
    ]
    
    # Processa os resultados à medida que completam
    for future in as_completed(futures):
        result = future.result()
        if "error" in result:
            print(f"Erro ao acessar {result['url']}: {result['error']}")
        else:
            print(f"Status Code: {result['status_code']} | URL: {result['url']} | Response: {result['data']}")

