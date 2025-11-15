from flask import Flask, render_template, redirect, request, url_for
from acesso_db import DBManager
from models import Pergunta, Avaliacao, Resposta
from datetime import datetime, timezone
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
@app.route("/pedidos/avaliar/<int:id_pedido>", methods=["GET", "POST"])
def avaliar_pedido(id_pedido):

    if request.method == "GET":
        pedido = db.buscar_pedido_por_id(id_pedido)
        itens_pedido = db.buscar_itens_pedido_por_id_pedido(id_pedido)
        valor_total_pedido = sum(item.quantidade * item.preco_unidade for item in itens_pedido)

        p_entregador = db.buscar_pergunta_aleatoria_por_alvo("entregador")
        p_estabelecimento = db.buscar_pergunta_aleatoria_por_alvo("estabelecimento")
        p_aplicativo = db.buscar_pergunta_aleatoria_por_alvo("aplicativo")


        p_itens_pedido = []
        for item in itens_pedido:
            p_itens_pedido.append({"id_item_pedido" : item.id,
                                   "nome_item" : item.item.nome,
                                   "pergunta" : db.buscar_pergunta_aleatoria_por_alvo("item_do_pedido")}
            )

        return render_template("avaliar_pedido.html",
                               pedido=pedido,
                               itens_pedido=itens_pedido,
                               total=valor_total_pedido,
                               p_entregador=p_entregador,
                               p_estabelecimento=p_estabelecimento,
                               p_aplicativo=p_aplicativo,
                               p_itens_pedido=p_itens_pedido,
                )

    if request.method == "POST":
        avaliacao = Avaliacao(None, datetime.now(timezone.utc), db.buscar_pedido_por_id(id_pedido))
        respostas = []

        for chave, valor_resposta in request.form.items():

            partes = chave.split("_")

            if not partes[0] == "resposta":
                continue

            alvo_avaliacao = partes[1]
            id_pergunta = int(partes[-1])
            pergunta_obj = db.buscar_pergunta_por_id(id_pergunta)

            item_pedido_obj = None

            if alvo_avaliacao == "item":
                id_item_pedido = int(partes[2])
                item_pedido_obj = db.buscar_item_do_pedido_por_id(id_item_pedido)

            resposta = Resposta(None, avaliacao, pergunta_obj, item_pedido_obj, valor_resposta)
            respostas.append(resposta)

        db.salvar_avaliacao_atomica(avaliacao, respostas)
        return redirect(f"/pedidos/avaliar/{id_pedido}", code=302)




app.run(debug=True)