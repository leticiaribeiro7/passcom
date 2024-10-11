from flask import Flask
from prisma import Prisma, register

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

@app.route("/teste")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
  app.run(debug=True, port=5000, host='0.0.0.0')