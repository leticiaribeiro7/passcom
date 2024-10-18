# Usando uma imagem oficial do Python
FROM python:3.12-slim

# Definindo diretório de trabalho dentro do container
WORKDIR /app

# Copiando os arquivos de dependências
COPY requirements.txt .

# Instalando as dependências
RUN pip install --upgrade -r requirements.txt

# Copiando o restante do código para o container
COPY . .

COPY prisma/schema.prisma ./prisma/schema.prisma

# RUN prisma generate

# RUN prisma migrate dev --name "init"
RUN chmod +x start.sh

ENV FLASK_APP=main.py

# Comando para rodar a aplicação Flask
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

CMD ["./start.sh"]