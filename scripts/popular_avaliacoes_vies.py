import sys
import os
import random
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao.pedidos_dao import PedidosDAO
from app.dao.avaliacoes_dao import AvaliacoesDAO
from app.dao.perguntas_dao import PerguntasDAO

from app.models.avaliacoes import Avaliacao, Resposta

# --- CONFIGURAÇÃO DE VIÉS ---

RANGES_BOM_EST = [range(300, 310), range(374, 383), range(424, 429)]
RANGES_RUIM_EST = [range(237, 247), range(310, 318), range(383, 389)]

RANGES_BOM_ENT = [range(96, 101)]
RANGES_RUIM_ENT = [range(1, 6)]

ITENS_BOM = ["X-Salada", "Margherita", "Mocca"]
ITENS_RUIM = ["X-Tudo", "4 Queijos", "Latte"]


def definir_pesos_nota_est(id_estabelecimento=None, nome_item=None):
    # Retorna uma lista de 5 pesos enviesados, partindo desses pesos padrao abaixo

    pesos_1_5 = [0.1, 0.1, 0.3, 0.3, 0.2]
    pesos_s_n = [0.5, 0.5]

    # 1. Viés de Estabelecimento
    if id_estabelecimento:
        is_bom = any(id_estabelecimento in r for r in RANGES_BOM_EST)
        is_ruim = any(id_estabelecimento in r for r in RANGES_RUIM_EST)

        if is_bom:
            return [0.05, 0.05, 0.15, 0.35, 0.4], [0.2, 0.8]
        if is_ruim:
            return [0.35, 0.35, 0.2, 0.05, 0.05], [0.7, 0.3]

    # 2. Viés de Item
    if nome_item:
        if nome_item in ITENS_BOM:
            return [0.05, 0.05, 0.15, 0.35, 0.4], [0.2, 0.8]
        if nome_item in ITENS_RUIM:
            return [0.35, 0.35, 0.2, 0.05, 0.05], [0.7, 0.3]

    return pesos_1_5, pesos_s_n

def definir_pesos_nota_ent(id_entregador=None):

    pesos_1_5 = [0.1, 0.1, 0.3, 0.3, 0.2]
    pesos_s_n = [0.5, 0.5]

    # 1. Viés de Estabelecimento
    if id_entregador:
        is_bom = id_entregador in RANGES_BOM_ENT
        is_ruim = id_entregador in RANGES_RUIM_ENT

        if is_bom:
            return [0.05, 0.05, 0.15, 0.35, 0.4], [0.2, 0.8]
        if is_ruim:
            return [0.35, 0.35, 0.2, 0.05, 0.05], [0.7, 0.3]

    return pesos_1_5, pesos_s_n

def gerar_valor_resposta(tipo_pergunta, pesos_1_5, pesos_s_n):
    # Gera o valor final da resposta (texto) baseado no tipo e nos pesos.
    if tipo_pergunta == "nota_1_5":
        opcoes = ["1", "2", "3", "4", "5"]
        return random.choices(opcoes, weights=pesos_1_5, k=1)[0]

    elif tipo_pergunta == "sim_nao":
        return random.choices(["sim", "nao"], weights=pesos_s_n, k=1)[0]

    else:
        return "Avaliação gerada automaticamente."

# FUNÇÃO PRINCIPAL

def popular_avaliacoes():
    print("--- Iniciando População de Avaliações com Viés ---")

    pedidos_dao = PedidosDAO()
    perguntas_dao = PerguntasDAO()
    avaliacoes_dao = AvaliacoesDAO()

    pedidos = pedidos_dao.buscar_pedidos_para_avaliar()

    if not pedidos:
        print("Nenhum pedido 'Concluído' encontrado para avaliar.")
        return

    print(f"Encontrados {len(pedidos)} pedidos para avaliar.")
    count_sucesso = 0

    for pedido in pedidos:
        try:
            respostas_para_salvar = []

            id_est = pedido.estabelecimento.id
            id_entregador = pedido.entregador.id
            pesos_est_1_5, pesos_est_s_n = definir_pesos_nota_est(id_estabelecimento=id_est)
            pesos_ent_1_5, pesos_ent_s_n = definir_pesos_nota_ent(id_entregador=id_entregador)

            # --- PERGUNTA 1: ENTREGADOR ---
            p_ent = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("entregador")
            if p_ent:
                val = gerar_valor_resposta(p_ent.tipo_resposta, pesos_1_5=pesos_ent_1_5, pesos_s_n=pesos_ent_s_n)
                respostas_para_salvar.append(
                    Resposta(id=None, avaliacao_obj=None, pergunta_obj=p_ent, item_pedido_obj=None, valor_resposta=val))

            # --- PERGUNTA 2: ESTABELECIMENTO ---
            p_est = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("estabelecimento")
            if p_est:
                val = gerar_valor_resposta(p_est.tipo_resposta, pesos_est_1_5, pesos_est_s_n)
                respostas_para_salvar.append(
                    Resposta(id=None, avaliacao_obj=None, pergunta_obj=p_est, item_pedido_obj=None, valor_resposta=val))

            # --- PERGUNTA 3: APLICATIVO ---
            p_app = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("aplicativo")
            if p_app:
                # Viés Neutro/Positivo
                val = gerar_valor_resposta(p_app.tipo_resposta, [0.1, 0.1, 0.2, 0.3, 0.3], [0.5, 0.5])
                respostas_para_salvar.append(
                    Resposta(id=None, avaliacao_obj=None, pergunta_obj=p_app, item_pedido_obj=None, valor_resposta=val))

            # --- PERGUNTAS 4: ITENS DO PEDIDO ---
            itens_pedido_objs = pedidos_dao.buscar_itens_pedido_por_id_pedido(pedido.id)

            for ip_obj in itens_pedido_objs:
                p_item = perguntas_dao.buscar_pergunta_aleatoria_por_alvo("item_do_pedido")
                if p_item:
                    pesos_item_1_5, pesos_item_s_n = definir_pesos_nota_est(nome_item=ip_obj.item.classe_produto.tipo_produto)
                    val = gerar_valor_resposta(p_item.tipo_resposta, pesos_item_1_5, pesos_item_s_n)

                    respostas_para_salvar.append(
                        Resposta(id=None, avaliacao_obj=None, pergunta_obj=p_item, item_pedido_obj=ip_obj,
                                 valor_resposta=val))

            # --- SALVAR TUDO ATOMICAMENTE ---
            if respostas_para_salvar:
                nova_avaliacao = Avaliacao(id=None, data_hora=datetime.now(), pedido_obj=pedido)

                avaliacoes_dao.salvar_avaliacao_atomica(nova_avaliacao, respostas_para_salvar)
                count_sucesso += 1

                if count_sucesso % 10 == 0:
                    print(f"Processados {count_sucesso} pedidos...")

        except Exception as e:
            print(f"Erro ao avaliar pedido {pedido.id}: {e}")
            break

    print("-" * 30)
    print(f"População concluída! {count_sucesso} avaliações geradas.")


if __name__ == "__main__":
    popular_avaliacoes()