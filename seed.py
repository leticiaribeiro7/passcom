import os
from prisma import Prisma

# Inicializando o cliente Prisma
db = Prisma()
db.connect()

def seed(company: str):
    if company == "a":
        # Criando usuários para Companhia A
        user_a1 = db.user.create(
            data={
                "login": "usuario_a1",
                "password": "senha_a1"
            }
        )
        
        user_a2 = db.user.create(
            data={
                "login": "usuario_a2",
                "password": "senha_a2"
            }
        )

        # Criando trechos para Companhia A
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

        # Criando assentos para os trechos da Companhia A
        for i in range(1, 6):
            db.assento.create(
                data={
                    "numero": i,
                    "id_trecho": trecho_a1.id,
                    "disponivel": 1  # 1 = disponível
                }
            )
            db.assento.create(
                data={
                    "numero": i+1,
                    "id_trecho": trecho_a2.id,
                    "disponivel": 1  # 1 = disponível
                }
            )

        # Criando passagens para Companhia A
        passagem_a1 = db.passagem.create(
            data={
                "uuid": "uuid-a1",
                "user_id": user_a1.id
            }
        )

        passagem_a2 = db.passagem.create(
            data={
                "uuid": "uuid-a2",
                "user_id": user_a2.id
            }
        )

        # Reservando trechos da Companhia A
        db.trechoreservado.create(
            data={
                "uuid_passagem": passagem_a1.uuid,
                "id_trecho": trecho_a1.id,
                "id_assento": 1
            }
        )

        db.trechoreservado.create(
            data={
                "uuid_passagem": passagem_a2.uuid,
                "id_trecho": trecho_a2.id,
                "id_assento": 2
            }
        )

    elif company == "b":
        # Criando usuários para Companhia B
        user_b1 = db.user.create(
            data={
                "login": "usuario_b1",
                "password": "senha_b1"
            }
        )
        
        user_b2 = db.user.create(
            data={
                "login": "usuario_b2",
                "password": "senha_b2"
            }
        )

        # Criando trechos para Companhia B
        trecho_b1 = db.trecho.create(
            data={
                "origem": "Cidade A3",
                "destino": "Cidade B3",
                "company": "b"
            }
        )
        
        trecho_b2 = db.trecho.create(
            data={
                "origem": "Cidade A4",
                "destino": "Cidade B4",
                "company": "b"
            }
        )

        # Criando assentos para os trechos da Companhia B
        for i in range(1, 6):
            db.assento.create(
                data={
                    "numero": i,
                    "id_trecho": trecho_b1.id,
                    "disponivel": 1  # 1 = disponível
                }
            )
            db.assento.create(
                data={
                    "numero": i,
                    "id_trecho": trecho_b2.id,
                    "disponivel": 1  # 1 = disponível
                }
            )

        # Criando passagens para Companhia B
        passagem_b1 = db.passagem.create(
            data={
                "uuid": "uuid-b1",
                "user_id": user_b1.id
            }
        )

        passagem_b2 = db.passagem.create(
            data={
                "uuid": "uuid-b2",
                "user_id": user_b2.id
            }
        )

        # Reservando trechos da Companhia B
        db.trechoreservado.create(
            data={
                "uuid_passagem": passagem_b1.uuid,
                "id_trecho": trecho_b1.id,
                "id_assento": 1
            }
        )

        db.trechoreservado.create(
            data={
                "uuid_passagem": passagem_b2.uuid,
                "id_trecho": trecho_b2.id,
                "id_assento": 2
            }
        )

    db.disconnect()

if __name__ == "__main__":
    company_arg = os.getenv("COMPANY_NAME")  # Exemplo: 'a' ou 'b'
    seed(company_arg)
