import os
from prisma import Prisma

db = Prisma()
db.connect()

def seed(company):
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

    # Criando trechos específicos para cada companhia com cidades reais e trechos complementares
    if company == "a":
        # Trechos para Companhia A
        trecho_sp_rj = db.trecho.create(
            data={
                "origem": "São Paulo",
                "destino": "Rio de Janeiro",
                "company": "a"
            }
        )
        trecho_rj_cwb = db.trecho.create(
            data={
                "origem": "Rio de Janeiro",
                "destino": "Curitiba",
                "company": "a"
            }
        )
        # Assentos para os trechos da Companhia A
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_sp_rj.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_rj_cwb.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia A
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_1.uuid, "id_trecho": trecho_sp_rj.id, "id_assento": 1}
        )

    elif company == "b":
        # Trechos para Companhia B
        trecho_cwb_po = db.trecho.create(
            data={
                "origem": "Curitiba",
                "destino": "Porto Alegre",
                "company": "b"
            }
        )
        trecho_po_florianopolis = db.trecho.create(
            data={
                "origem": "Porto Alegre",
                "destino": "Florianópolis",
                "company": "b"
            }
        )
        # Assentos para os trechos da Companhia B
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_cwb_po.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_po_florianopolis.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia B
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_1.uuid, "id_trecho": trecho_cwb_po.id, "id_assento": 2}
        )

    elif company == "c":
        # Trechos para Companhia C
        trecho_florianopolis_sp = db.trecho.create(
            data={
                "origem": "Florianópolis",
                "destino": "São Paulo",
                "company": "c"
            }
        )
        trecho_sp_bh = db.trecho.create(
            data={
                "origem": "São Paulo",
                "destino": "Belo Horizonte",
                "company": "c"
            }
        )
        # Assentos para os trechos da Companhia C
        for i in range(1, 6):
            db.assento.create(data={"numero": i, "id_trecho": trecho_florianopolis_sp.id, "disponivel": 1})
            db.assento.create(data={"numero": i, "id_trecho": trecho_sp_bh.id, "disponivel": 1})

        # Reservando trechos compartilhados em Companhia C
        db.trechoreservado.create(
            data={"uuid_passagem": passagem_shared_2.uuid, "id_trecho": trecho_florianopolis_sp.id, "id_assento": 3}
        )

    db.disconnect()

if __name__ == "__main__":
    company = os.getenv("COMPANY_NAME")  # Exemplo: 'a', 'b', ou 'c'
    seed(company)
