from datetime import datetime, timezone

from flask import Blueprint, render_template, request, redirect, url_for
from app.dao import PerguntasDAO, PedidosDAO, AvaliacoesDAO
from app.models import Pergunta, Avaliacao, Resposta

bp = Blueprint('avaliacoes', __name__)
perguntas_dao = PerguntasDAO()
pedidos_dao = PedidosDAO()
avaliacoes_dao = AvaliacoesDAO()

@bp.route("/cadastro/perguntas", methods=["GET", "POST"])
def cadastrar_perguntas():
    if request.method == "POST":
        enunciado = request.form.get("enunciado_pergunta")
        alvo_avaliacao = request.form.get("alvo_avaliacao")
        tipo_resposta = request.form.get("tipo_resposta")
        pergunta = Pergunta(None, enunciado, tipo_resposta, alvo_avaliacao)
        perguntas_dao.inserir_pergunta(pergunta)
        return redirect(url_for("gerenciar"))

    if request.method == "GET":
        return render_template("cadastro_perguntas.html")

@bp.route("/pedidos/avaliar/<int:id_pedido>", methods=["GET", "POST"])
def avaliar_pedido(id_pedido):

    if request.method == "GET":
        pedido = pedidos_dao.buscar_pedido_por_id(id_pedido)
        itens_pedido = pedidos_dao.buscar_itens_pedido_por_id_pedido(id_pedido)
        valor_total_pedido = sum(item.quantidade * item.preco_unidade for item in itens_pedido)

        p_entregador = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("entregador")
        p_estabelecimento = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("estabelecimento")
        p_aplicativo = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("aplicativo")

        p_itens_pedido = []
        for item in itens_pedido:
            p_itens_pedido.append({"id_item_pedido": item.id,
                                   "nome_item": item.item.nome,
                                   "pergunta": perguntas_dao.buscar_pergunta_aleatoria_por_alvo("item_do_pedido")}
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
        avaliacao = Avaliacao(None, datetime.now(timezone.utc), pedidos_dao.buscar_pedido_por_id(id_pedido))
        respostas = []

        for chave, valor_resposta in request.form.items():

            partes = chave.split("_")

            if not partes[0] == "resposta":
                continue

            alvo_avaliacao = partes[1]
            id_pergunta = int(partes[-1])
            pergunta_obj = perguntas_dao.buscar_pergunta_por_id(id_pergunta)

            item_pedido_obj = None

            if alvo_avaliacao == "item":
                id_item_pedido = int(partes[2])
                item_pedido_obj = pedidos_dao.buscar_item_do_pedido_por_id(id_item_pedido)

            resposta = Resposta(None, avaliacao, pergunta_obj, item_pedido_obj, valor_resposta)
            respostas.append(resposta)

        avaliacoes_dao.salvar_avaliacao_atomica(avaliacao, respostas)
        return redirect("/pedidos", code=302)
