import os
from prisma import Prisma

# Inicializando o cliente Prisma
db = Prisma()
db.connect()

def seed(company: str):
    # Criando usuários compartilhados
    user_shared_1 = db.user.upsert(
        where={"login": "usuario_shared_1"},
        data={
            "create": {"login": "usuario_shared_1", "password": "senha1", "uuid": "uuid1"},
            "update": {}
        }
    )

    user_shared_2 = db.user.upsert(
        where={"login": "usuario_shared_2"},
        data={
            "create": {"login": "usuario_shared_2", "password": "senha2", "uuid": "uuid2"},
            "update": {}
        }
    )

    # Criando passagens compartilhadas
    passagem_shared_1 = db.passagem.upsert(
        where={"uuid": "uuid-shared-1"},
        data={
            "create": {"uuid": "uuid-shared-1", "user_uuid": user_shared_1.uuid},
            "update": {}
        }
    )

    passagem_shared_2 = db.passagem.upsert(
        where={"uuid": "uuid-shared-2"},
        data={
            "create": {"uuid": "uuid-shared-2", "user_uuid": user_shared_2.uuid},
            "update": {}
        }
    )

    # Criando trechos específicos para cada companhia
    if company == "a":
        # Trechos para Companhia A
        trecho_a1 = db.trecho.create(
            data={
                "origem": "Cidade A1",
                "destino": "Cidade B1",
                "company": "a"
            }
        )
        trecho_a2 = db.trecho.create(
            data={
                "origem": "Cidade A2",
                "destino": "Cidade B2",
                "company": "a"
            }
        )
        # Assentos para os trechos da Companhia A
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_a1.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_a2.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia A
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_1.uuid, "id_trecho": trecho_a1.id, "id_assento": 1}
        )

    elif company == "b":
        # Trechos para Companhia B
        trecho_b1 = db.trecho.create(
            data={
                "origem": "Cidade B1",
                "destino": "Cidade C1",
                "company": "b"
            }
        )
        trecho_b2 = db.trecho.create(
            data={
                "origem": "Cidade B2",
                "destino": "Cidade C2",
                "company": "b"
            }
        )
        # Assentos para os trechos da Companhia B
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_b1.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_b2.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia B
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_1.uuid, "id_trecho": trecho_b1.id, "id_assento": 2}
        )


    elif company == "c":
        # Trechos para Companhia C
        trecho_c1 = db.trecho.create(
            data={
                "origem": "Cidade C1",
                "destino": "Cidade D1",
                "company": "c"
            }
        )
        trecho_c2 = db.trecho.create(
            data={
                "origem": "Cidade C2",
                "destino": "Cidade D2",
                "company": "c"
            }
        )
        # Assentos para os trechos da Companhia C
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_c1.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_c2.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia C
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_2.uuid, "id_trecho": trecho_c1.id, "id_assento": 3}
        )

    db.disconnect()

if __name__ == "__main__":
    company_arg = os.getenv("COMPANY_NAME")  # Exemplo: 'a', 'b', ou 'c'
    seed(company_arg)
