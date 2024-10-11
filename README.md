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

<!-- cria um a cada reserva completa - forma uma passagem -->
- passagem
    - id
    - user_id - foreign
    - created_at    TIMESTAMP

<!-- cria um a cada trecho -->
- trechos_reservados
    - id
    - passagem_id - foreign
    - trecho_id
    - assento_id


<!-- flask --app main run     -->
