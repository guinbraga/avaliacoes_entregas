from flask import Flask, render_template, redirect, request
from acesso_db import DBManager
from models import Pergunta

app = Flask(__name__)
db = DBManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerenciar")
def gerenciar():
    return render_template("gerenciar.html")

@app.route("/cadastro/perguntas")
def cadastrar_perguntas():
    enunciado = request.args["enunciado_pergunta"]
    alvo_avaliacao = request.args["alvo_avaliacao"]
    tipo_resposta = request.args["tipo_resposta"]
    pergunta = Pergunta(None, enunciado, tipo_resposta, alvo_avaliacao)
    db.inserir_pergunta(pergunta)


    return render_template("cadastro_perguntas.html")

@app.route("/pedido/avaliar/<int:id_pedido>")
def avaliar_pedido(id_pedido):
    pedido = db.buscar_pedido_por_id(id_pedido)
    itens_pedido = db.buscar_itens_pedido_por_id(id_pedido)


app.run(debug=True)