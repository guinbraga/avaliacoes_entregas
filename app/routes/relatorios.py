# app/routes/relatorios.py
from flask import render_template, Blueprint
from app.dao.relatorios_dao.rel_estabelecimentos_dao import RelEstabelecimentosDao

bp = Blueprint('relatorios', __name__)

@bp.route("/dashboard")
def dashboard():
    dao = RelEstabelecimentosDao()
    dados_top_produtos = dao.top_5_nota_1_5(("Qual nota você dá para o estabelecimento?",))

    labels_produtos = [linha[1] for linha in dados_top_produtos]

    valores_produtos = [linha[0] for linha in dados_top_produtos]

    return render_template(
        "dashboard.html",
        labels_grafico_1=labels_produtos,
        valores_grafico_1=valores_produtos
    )