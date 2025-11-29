from app.models import Estabelecimento, Entregador, Cliente, Pedido, Item_pedido
from . import ItensDAO
from .base import get_db_connection

class PedidosDAO:

    def inserir_pedido(self, pedido, itens_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO pedidos (id_estabelecimento, id_cliente, data_hora, status, id_entregador)
                                VALUES (%s, %s, %s, %s, %s)
                                RETURNING id_pedido;
                                """,
                                (pedido.estabelecimento.id, pedido.cliente.id, pedido.data_hora, pedido.status,
                                 pedido.entregador.id)
                                )

                    id_pedido = cur.fetchone()[0]
                    pedido.id = id_pedido

                    for item_pedido in itens_pedido:
                        item_pedido.pedido_obj = pedido
                        cur.execute("""
                                    INSERT INTO itens_pedido (id_pedido, id_item, quantidade, preco_unidade)
                                    VALUES (%s, %s, %s, %s)
                                    RETURNING id_item_pedido;
                                    """, (item_pedido.pedido.id, item_pedido.item.id, item_pedido.quantidade,
                                          item_pedido.preco_unidade))
                        id_item_pedido = cur.fetchone()[0]
                        item_pedido.id = id_item_pedido

                    conn.commit()

                except Exception as e:
                    print("Erro ao inserir pedido:")
                    print(e)
                    conn.rollback()

    def inserir_item_pedido(self, item_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO itens_pedido (id_pedido, id_item, quantidade, preco_unidade)
                                VALUES (%s, %s, %s, %s) RETURNING id_item_pedido;
                                """,
                                (item_pedido.pedido.id, item_pedido.item.id, item_pedido.quantidade, item_pedido.preco_unidade)
                    )
                    id_item_pedido = cur.fetchone()[0]
                    item_pedido.id = id_item_pedido
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_pedidos_para_avaliar(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT p.id_pedido, p.data_hora, p.status,
                                    e.id_estabelecimento, e.cnpj, e.nome AS nome_estabelecimento, e.endereco AS endereco_estabelecimento,
                                    en.id_entregador, en.nome AS nome_entregador, en.cpf AS cpf_entregador,
                                    c.id_cliente, c.cpf AS cliente_cpf, c.endereco AS cliente_endereco, c.sexo, c.nome AS cliente_nome
                                FROM pedidos p 
                                JOIN estabelecimentos e ON p.id_estabelecimento = e.id_estabelecimento
                                JOIN clientes c ON p.id_cliente = c.id_cliente
                                JOIN entregadores en ON p.id_entregador = en.id_entregador
                                WHERE p.status = 'Concluído'
                                """)
                    query = cur.fetchall()
                    if not query:
                        print("Nenhum pedido encontrado!")
                        return None
                    else:
                        lista_pedidos = []
                        for resultado in query:
                            estabelecimento_obj = Estabelecimento(
                                id=resultado[3], cnpj=resultado[4], nome=resultado[5], endereco=resultado[6]
                            )
                            entregador_obj = Entregador(
                                id=resultado[7], nome=resultado[8], cpf=resultado[9]
                            )
                            cliente_obj = Cliente(
                                id=resultado[10], cpf=resultado[11], endereco=resultado[12], sexo=resultado[13], nome=resultado[14]
                            )
                            pedido_obj = Pedido(
                                id=resultado[0],
                                estabelecimento_obj=estabelecimento_obj,
                                entregador_obj=entregador_obj,
                                cliente_obj=cliente_obj,
                                data_hora=resultado[1],
                                status=resultado[2]
                            )
                            lista_pedidos.append(pedido_obj)
                except Exception as e:
                    print(e)
                    return None

        return lista_pedidos

    def buscar_pedido_por_id(self, id_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT p.id_pedido, p.data_hora, p.status,
                                        e.id_estabelecimento, e.cnpj, e.nome AS estabelecimento_nome, e.endereco AS endereco_estabelecimento,
                                        en.id_entregador, en.nome AS nome_entregador, en.cpf AS cpf_entregador,
                                        c.id_cliente, c.cpf AS cliente_cpf, c.endereco AS cliente_endereco, c.sexo, c.nome AS cliente_nome
                                    FROM pedidos p
                                    JOIN estabelecimentos e ON p.id_estabelecimento = e.id_estabelecimento
                                    JOIN entregadores en ON p.id_entregador = en.id_entregador
                                    JOIN clientes c ON p.id_cliente = c.id_cliente
                                    WHERE p.id_pedido = (%s)
                    """, (id_pedido,)
                    )

                    resultado = cur.fetchone()
                    if not resultado:
                        print(f"Nenhum pedido encontrado com id {id_pedido}")
                        return None

                    estabelecimento_obj = Estabelecimento(
                        id=resultado[3], cnpj=resultado[4], nome=resultado[5], endereco=resultado[6]
                    )

                    entregador_obj = Entregador(
                        id=resultado[7], nome=resultado[8], cpf=resultado[9]
                    )

                    cliente_obj = Cliente(
                        id=resultado[10], cpf=resultado[11], endereco=resultado[12], sexo=resultado[13], nome=resultado[14]
                    )

                    pedido_obj = Pedido(
                        id=resultado[0], data_hora=resultado[1], status=resultado[2],
                        estabelecimento_obj=estabelecimento_obj,
                        entregador_obj=entregador_obj,
                        cliente_obj=cliente_obj
                    )
                except Exception as e:
                    print(e)
                    return None

        return pedido_obj

    def buscar_itens_pedido_por_id_pedido(self, id_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(""" SELECT id_item_pedido, id_pedido, id_item, quantidade, preco_unidade
                                FROM itens_pedido WHERE id_pedido = (%s)""", (id_pedido,)
                                )
                    resultado = cur.fetchall()
                    itens_pedido = []
                    pedido_obj = self.buscar_pedido_por_id(id_pedido)
                    itens_dao = ItensDAO()

                    for item in resultado:
                        item_obj = itens_dao.buscar_item_por_id(item[2])
                        item_pedido = Item_pedido(item[0], pedido_obj, item_obj, item[3], item[4])
                        itens_pedido.append(item_pedido)

                    return itens_pedido

                except Exception as e:
                    print(e)

    def buscar_item_do_pedido_por_id(self, id_item_pedido):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(""" SELECT id_item_pedido, id_pedido, id_item, quantidade, preco_unidade
                                FROM itens_pedido WHERE id_item_pedido = (%s)""", (id_item_pedido,)
                                )
                    resultado = cur.fetchone()
                    if not resultado:
                        print(f"Nenhum item de pedido encontrado com id {id_item_pedido}")
                        return None

                    itens_dao = ItensDAO()
                    pedido_obj = self.buscar_pedido_por_id(resultado[1])
                    item_obj = itens_dao.buscar_item_por_id(resultado[2])

                    item_pedido = Item_pedido(resultado[0], pedido_obj, item_obj, resultado[3], resultado[4])

                    return item_pedido

                except Exception as e:
                    print(e)
                    return None