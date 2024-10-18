from flask import Flask, jsonify
from prisma import Prisma, register

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

# teste criando um trecho
db.trecho.create(data={'origem': 'SSA', 'destino': 'SP'})

@app.route("/trechos")
def get_trechos():
  trechos = db.trecho.find_many()
  return {
      "data": [trecho.dict() for trecho in trechos]
  }


if __name__ == "__main__":
  app.run(debug=True, port=5000, host='0.0.0.0')