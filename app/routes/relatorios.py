# app/routes/relatorios.py
from flask import render_template, Blueprint, request
from app.dao.relatorios_dao.rel_estabelecimentos_dao import RelEstabelecimentosDao

bp = Blueprint('relatorios', __name__)
pergunta_nota_estabelecimento = "Qual nota você dá para o estabelecimento?"
pergunta_tempo_preparo = "O tempo de preparo do seu pedido foi adequado?"

# Em app/routes/relatorios.py

@bp.route("/dashboard")
def dashboard():
    dao = RelEstabelecimentosDao()

    # 1. Pegar filtro da URL (preparando para o futuro)
    categoria_arg = request.args.get('categoria')

    if not categoria_arg or categoria_arg == 'geral':
        categoria_selecionada = None

    else:
        categoria_selecionada = categoria_arg

    # Gráfico 1: Maiores Notas
    dados_m_notas_brutos = dao.top_5_nota_1_5(
        enunciado_pergunta=pergunta_nota_estabelecimento,
        categoria=categoria_selecionada
    )
    labels_maiores_notas = [dado[1] for dado in dados_m_notas_brutos]
    dados_maiores_notas = [dado[0] for dado in dados_m_notas_brutos]

    # Gráfico 2: Melhor Percepção de Tempo
    dados_mt_brutos = dao.top_5_prop_sim_nao(
        enunciado_pergunta=pergunta_tempo_preparo,
        categoria=categoria_selecionada
    )
    labels_melhor_tempo = [dado[1] for dado in dados_mt_brutos]
    dados_melhor_tempo = [dado[0] for dado in dados_mt_brutos]

    # Gráfico 3: Piores Notas
    dados_p_notas_brutos = dao.pior_5_nota_1_5(
        enunciado_pergunta=pergunta_nota_estabelecimento,
        categoria=categoria_selecionada
    )
    labels_piores_notas = [dado[1] for dado in dados_p_notas_brutos]
    dados_piores_notas = [dado[0] for dado in dados_p_notas_brutos]

    # Gráfico 4: Pior Tempo
    dados_pt_brutos = dao.pior_5_prop_sim_nao(
        enunciado_pergunta=pergunta_tempo_preparo,
        categoria=categoria_selecionada)
    labels_pior_tempo = [dado[1] for dado in dados_pt_brutos]
    dados_pior_tempo = [dado[0] for dado in dados_pt_brutos]

    # KPIs
    qtd_acima_media = dao.count_est_acima(3.5, categoria_selecionada)
    total_estabelecimentos = dao.total_estabelecimentos(categoria_selecionada)
    dados_item_preferido = dao.melhor_item(categoria_selecionada)
    item_preferido_nome = dados_item_preferido[0]
    item_preferido_est = dados_item_preferido[1]
    item_preferido_nota = dados_item_preferido[2]

    return render_template(
        "relatorios/dashboard.html",
        # Passando as variáveis
        labels_maiores_notas=labels_maiores_notas,
        dados_maiores_notas=dados_maiores_notas,
        labels_melhor_tempo=labels_melhor_tempo,
        dados_melhor_tempo=dados_melhor_tempo,
        labels_piores_notas=labels_piores_notas,
        dados_piores_notas=dados_piores_notas,
        labels_pior_tempo=labels_pior_tempo,
        dados_pior_tempo=dados_pior_tempo,
        qtd_acima_media=qtd_acima_media,
        item_preferido_nome=item_preferido_nome,
        item_preferido_nota=item_preferido_nota,
        item_preferido_est=item_preferido_est,
        total_estabelecimentos=total_estabelecimentos,
    )