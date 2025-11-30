import sys
import os
import random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao.base import get_db_connection
from app.dao.pedidos_dao import PedidosDAO

from app.models.pedidos import Pedido, Item_pedido
from app.models.itens import Item
from app.models.usuarios import Cliente, Entregador
from app.models.estabelecimentos import Estabelecimento


def popular_pedidos_massa(n):
    print("--- Iniciando População de Pedidos em Massa ---")

    pedidos_dao = PedidosDAO()

    lista_clientes = []
    lista_entregadores = []
    lista_estabelecimentos = []

    conn = get_db_connection()
    if not conn:
        print("Erro de conexão.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_cliente, nome, cpf, endereco, sexo FROM clientes")
            for row in cur.fetchall():
                lista_clientes.append(Cliente(id=row[0], nome=row[1], cpf=row[2], endereco=row[3], sexo=row[4]))

            cur.execute("SELECT id_entregador, nome, cpf FROM entregadores")
            for row in cur.fetchall():
                lista_entregadores.append(Entregador(id=row[0], nome=row[1], cpf=row[2]))

            cur.execute("SELECT id_estabelecimento, nome, cnpj, endereco FROM estabelecimentos")
            for row in cur.fetchall():
                lista_estabelecimentos.append(
                    Estabelecimento(id=row[0], nome=row[1], cnpj=row[2], endereco=row[3] if len(row) > 3 else ""))


        total_pedidos_criados = 0

        for est in lista_estabelecimentos:
            print(f"Processando estabelecimento: {est.nome}...")

            # Buscar itens deste estabelecimento
            itens_deste_est = []
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_item, nome, valor_base, classificacao, id_estabelecimento
                            FROM itens
                            WHERE id_estabelecimento = %s
                            """, (est.id,))

                rows = cur.fetchall()
                for r in rows:
                    # Nota: passamos None para classe_produto e estabelecimento no Item pois não precisamos deles para o INSERT do pedido
                    itens_deste_est.append(Item(id=r[0], nome=r[1], valor_base=float(r[2]), classe_produto_obj=None,
                                                estabelecimento_obj=est))

            if not itens_deste_est:
                print(f"  -> PULEI: {est.nome} não tem itens cadastrados.")
                continue

            for i in range(n):

                cliente_sorteado = random.choice(lista_clientes)
                entregador_sorteado = random.choice(lista_entregadores)

                dias_atras = random.randint(0, 30)
                data_pedido = datetime.now() - timedelta(days=dias_atras)

                status = "Concluído"

                novo_pedido = Pedido(
                    id=None,
                    estabelecimento_obj=est,
                    cliente_obj=cliente_sorteado,
                    entregador_obj=entregador_sorteado,
                    data_hora=data_pedido,
                    status=status
                )

                try:
                    itens_deste_pedido = []
                    for item_obj in itens_deste_est:
                        novo_item_pedido = Item_pedido(
                            id=None,
                            pedido_obj=novo_pedido,
                            item_obj=item_obj,
                            quantidade=1,
                            preco_unidade=item_obj.valor_base  # O preço é o valor base
                        )
                        itens_deste_pedido.append(novo_item_pedido)

                    pedidos_dao.inserir_pedido(novo_pedido, itens_deste_pedido)

                    if not novo_pedido.id:
                        print("  -> Erro: DAO não retornou ID do pedido.")
                        continue

                    total_pedidos_criados += 1

                except Exception as e:
                    print(f"  -> Erro ao criar pedido {i} para {est.nome}: {e}")

        print("-" * 30)
        print(f"SCRIPT CONCLUÍDO. Total de pedidos gerados: {total_pedidos_criados}")

    except Exception as e:
        print(f"Erro fatal no script: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    popular_pedidos_massa(10)