<div align="center">
  <h1> PASSCOM - Venda de Passagens </h1>
  <h3>Universidade Estadual de Feira de Santana</h3>
  <h3> TEC502 - MI Concorrência e Conectividade</h3>
  <h4>Letícia Teixeira Ribeiro dos Santos, Lucca de Almeida Hora Coutinho</h4>
</div>

## Introdução

<p align="justify">
   
</p>

<p align="justify">
</p>

## Metodologia e Resultados

<p align="justify">

</p>
<p align="justify">
 
</p>

### Arquitetura da Solução


### Protocolo de Comunicação
<p align="justify">
    Toda a comunicação foi feita através de API REST e seguindo princípios stateless, em que cada requisição recebe todos os dados necessários para ser processada. Os endpoints são protegidos com autenticação JWT, os usuários precisam estar logados para realizar operações.
    Foram implementados dois conjuntos de rotas:
</p>

- **Comunicação entre servidores**
/register post
/trechos - get
/trecho-reservado - post
/trechos-reservados/<uuid_passagem> - delete
/assentos/<id> - put, get
/passagem - post
/passagem/user/<user_uuid> - get
/passagem/<user_uuid>/<passagem_uuid> - delete

- **Comunicação entre clientes e servidores**

#### 1. Cliente insere login e senha e recebe um token JWT para acessar o servidor atual. Todas as rotas do cliente necessitam do token.

**Requisição**
```
POST /login
Content-Type: application/json

{
    "login": "username1",
    "password": "password1"
}
```
**Resposta**
```
{
	"access_token": "eyJhbGciOi...iz9A"
}

```
#### 2. Cadastro do cliente no sistema


**Requisição**

```
POST /register-all
Content-Type: application/json

{
    "login": "username1",
    "password": "password1"
}
```
**Resposta**
```
{
    "message": "Usuário criado com sucesso"
}
```
#### 3. Busca trechos em todos os servidores, contém os assentos disponíveis de cada trecho 

**Requisição**
```
GET /all-trechos
Authorization: Bearer Token

```
**Resposta**
```
[
	{
		"assentos": [
			{
				"disponivel": 1,
				"id": 3,
				"numero": 2
			},
			{
				"disponivel": 1,
				"id": 5,
				"numero": 3
			}
		],
		"company": "a",
		"destino": "Cidade B1",
		"id": 1,
		"origem": "Cidade A1"
	}
]
```
#### 3. Cria uma passagem com os trechos e assentos escolhidos em todos os servidores 
**Requisição**
```
POST /reservar
Content-Type: application/json
Authorization: Bearer Token

{
    "user_uuid": "uuid2",
    "trechos": [
        {
            "id_trecho": 1,
            "id_assento": 9,
            "company": "a"
        },
        {
            "id_trecho": 2,
            "id_assento": 9,
            "company": "b"
        },
        {
            "id_trecho": 1,
            "id_assento": 9,
            "company": "c"
        }
    ]
}
```
**Resposta**
```
{
    "message": "Reserva efetuada com sucesso"
}
```

#### 4. Busca passagens do usuário através do seu UUID (identificador único)

**Requisição**
```
GET /passagens-all/<user_uuid>
Authorization: Bearer Token
```
**Resposta**
```
[
	{
		"created_at": "Wed, 30 Oct 2024 20:22:37 GMT",
		"trechosReservados": [
			{
				"assento": {
					"disponivel": 1,
					"numero": 2
				},
				"trecho": {
					"company": "c",
					"destino": "Cidade D1",
					"origem": "Cidade C1"
				}
			}
		],
		"uuid": "uuid-2"
	}
]
```

#### 5. Cancela passagem em todos os servidores através do UUID da passagem e do usuário
**Requisição**
```
DELETE /passagem-all/<user_uuid>/<passagem_uuid>
Authorization: Bearer Token
```
**Resposta**
```
{
    "message": "Passagem deletada com sucesso"
}
```




### Roteamento



### Concorrência Distribuída
<p align="justify">
</p>


<p align="justify">
</p>


### Confiabilidade da Solução
<p align="justify">
    Caso os servidores sejam desconectados e conectados novamente, os clientes não poderão continuar a operação que estavamfazendo e deve reiniciá-la ao se reconectar. Do ponto de vista da concorrência, o "lock" adquirido ao se solicitar a compra de uma passagem é liberado após 30 segundos em qualquer situação, para evitar que ocorram deadlocks. Além disso, a API foi desenvolvida seguindo o princípio Stateless, em que o estado do cliente não é armazenado entre requisições.
</p>


### Avaliação da Solução

### Documentação do Código

### Emprego do Docker
<p align="justify">
    Devido a necessidade de ter vários containers com serviços diferentes executando, foi usado o Docker Compose para gerenciá-los. Ao todo são 7 containers: 3 para os servidores das companhias, em que é executado o código da API; 3 para os bancos de dados de cada companhia; e 1 para o Redis que gerencia a concorrência distribuída. Todos os containers fazem parte da mesma rede e usam o driver Bridge, que permite a comunicação entre eles.
</p>

<p align="justify">
    A organização das dependências estão contidas no Dockerfile
    ;
</p>

## Conclusão

<p align="justify">
</p>

<p align="justify">
</p>

<p align="justify">
</p>
