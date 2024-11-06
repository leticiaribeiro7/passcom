FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

COPY prisma ./prisma

RUN chmod +x start.sh

ENV FLASK_APP=main.py

CMD ["./start.sh"]

