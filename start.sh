#!/bin/sh
prisma generate
prisma migrate dev --name "init"  # Executa a migração
flask run --host=0.0.0.0 --port=5000  # Executa o Flask
