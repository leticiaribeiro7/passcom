import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# URLs de login e dos servidores
login_urls = [
    "http://localhost:5000/login",  # Servidor A
    "http://localhost:5001/login",  # Servidor B
    "http://localhost:5002/login"   # Servidor C
]
server_urls = [
    "http://localhost:5000/all-trechos",  # Servidor A
    "http://localhost:5001/all-trechos",  # Servidor B
    "http://localhost:5002/all-trechos"   # Servidor C
]

# Credenciais para login
credentials = {"login": "usuario_shared_1", "password": "senha1"}

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

# Função para obter todos os trechos com autenticação
def get_all_trechos(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Espera-se que os trechos estejam no formato JSON
        else:
            print(f"Erro ao acessar {url}: {response.status_code} - {response.text}")
            return []
    except requests.RequestException as e:
        print(f"Erro ao conectar em {url}: {e}")
        return []

# Obtenção dos tokens para cada servidor
tokens = [get_jwt_token(url) for url in login_urls]

# Executor para gerenciar threads
with ThreadPoolExecutor(max_workers=len(server_urls)) as executor:
    # Cria uma lista de futuras chamadas para buscar os trechos de cada servidor
    futures = [executor.submit(get_all_trechos, url, tokens[i]) for i, url in enumerate(server_urls)]
    
    # Armazena todos os trechos de todos os servidores
    todos_trechos = []
    
    for future in as_completed(futures):
        result = future.result()
        todos_trechos.extend(result)

# Imprimir todos os trechos recebidos para depuração
print("Todos os trechos recebidos:")
for trecho in todos_trechos:
    print(trecho)

# Agora, vamos calcular as rotas
origem = "Sao Paulo"
destino = "Florianopolis"
rotas = []
rotas_unicas = set()  # Usar um conjunto para evitar duplicatas

# Função para buscar rotas recursivamente
def buscar_rotas(origem, destino, trechos, rota_atual):
    # Verifica se a origem atual é o destino
    if origem == destino:
        # Cria uma tupla imutável da rota atual para evitar duplicatas
        rota_tuple = tuple((trecho['origem'], trecho['destino'], trecho['company']) for trecho in rota_atual)
        rotas_unicas.add(rota_tuple)  # Adiciona a rota ao conjunto
        return
    
    # Busca todos os trechos que partem da origem atual
    for trecho in trechos:
        if trecho['origem'] == origem:
            # Adiciona o trecho à rota atual e faz uma busca recursiva
            buscar_rotas(trecho['destino'], destino, trechos, rota_atual + [trecho])

# Inicia a busca a partir de São Paulo
buscar_rotas(origem, destino, todos_trechos, [])

# Exibe todas as rotas únicas encontradas
print(f"\nRotas disponíveis de {origem} para {destino}:")
if rotas_unicas:
    for idx, rota in enumerate(rotas_unicas):
        print(f"Rota {idx + 1}:")
        for trecho in rota:
            print(f"- Trecho: {trecho[0]} para {trecho[1]} | Companhia: {trecho[2]}")
else:
    print("Nenhuma rota disponível.")
