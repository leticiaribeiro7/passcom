# passcom

/login
/logout
get /trechos -> ver rotas
delete /ticket -> cancelar passagem
post /ticket -> comprar passagem
get /ticket -> ver passagens

 <!-- o user será replicado em tds os servidores -->
DB tables:
- user
    - login
    - password
    - name

- assentos
    - id
    - numero
    - trecho_id - foreign

- trechos
    - id
    - origem
    - destino

<!-- cria um a cada reserva completa - forma uma passagem (atrela user a passagem) -->
- passagem
    - uuid
    - user_id - foreign
    - created_at    TIMESTAMP

<!-- cria um a cada trecho  (precisa pra quando for mostrar a passagem completa, mostrar tds os trechos da passagem) -->
- trechos_reservados
    - id
    - passagem_id - foreign
    - trecho_id
    - assento_id


<!-- flask --app main --debug run     -->
<!-- prisma migrate dev -->


<!-- docker compose up --build -->

<!-- A sua implementação apresenta características de topologia de malha parcial, já que permite que qualquer servidor busque dados de outros servidores. Contudo, a agregação de dados em um único ponto (endpoint /all-trechos) pode ser vista como uma característica de topologia de estrela. -->


<!-- formato req /reservar
{
    "user_uuid": "uuid1",
    "trechos": [
        {
            "id_trecho": 1,
            "id_assento": 1,
            "company": "a"
        },
        {
            "id_trecho": 2,
            "id_assento": 1,
            "company": "b"
        },
        {
            "id_trecho": 1,
            "id_assento": 1,
            "company": "c"
        }
    ]
}


-- migration sobe sem fazer alteraçao, faz a alteração, roda manual fora do docker, derruba tudo e sobe dnv