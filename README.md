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

**1.  Comunicação entre servidores**

/register - post
/trechos - get
/trecho-reservado - post
/trechos-reservados/<uuid_passagem> - delete
/assentos/<id> - put, get
/passagem - post
/passagem/user/<user_uuid> - get
/passagem/<user_uuid>/<passagem_uuid> - delete

**2.  Comunicação entre clientes e servidores**
/login
/register-all
/all-trechos - get
/passagem-all/<user_uuid>/<passagem_uuid> - delete
/passagens-all/<user_uuid> - get
/reservar - post

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