from flask import Flask, render_template

# código de ativação da interface web

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/passagens')
def passagens():
    return render_template('passagens.html')

@app.route('/rotas')
def rotas():
    return render_template('rotas.html')

@app.route('/opcoes')
def opcoes():
    return render_template('opcoes.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
