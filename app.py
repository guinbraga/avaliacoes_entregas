from flask import Flask, render_template, redirect, request, url_for
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

@app.route("/cadastro/perguntas", methods=["POST", "GET"])
def cadastrar_perguntas():
    if request.method == "POST":
        enunciado = request.form.get("enunciado_pergunta")
        alvo_avaliacao = request.form.get("alvo_avaliacao")
        tipo_resposta = request.form.get("tipo_resposta")
        pergunta = Pergunta(None, enunciado, tipo_resposta, alvo_avaliacao)
        db.inserir_pergunta(pergunta)
        return redirect(url_for("gerenciar"))

    if request.method == "GET":
        return render_template("cadastro_perguntas.html")

# @app.route("pedidos")
@app.route("/pedidos/avaliar/<int:id_pedido>")
def avaliar_pedido(id_pedido):
    pedido = db.buscar_pedido_por_id(id_pedido)
    itens_pedido = db.buscar_itens_pedido_por_id(id_pedido)
    valor_total_pedido = sum(item.quantidade * item.preco_unidade for item in itens_pedido)
    return render_template("avaliar_pedido.html",
                           pedido=pedido,
                           itens_pedido=itens_pedido,
                           total=valor_total_pedido)


app.run(debug=True)