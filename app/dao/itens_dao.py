from app.models import Classe_produto, Item
from . import EstabelecimentosDAO
from .base import get_db_connection

class ItensDAO:
    def inserir_item(self, item):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""INSERT INTO itens (nome, valor_base, classificacao, id_estabelecimento)
                                   VALUES (%s, %s, %s, %s)
                                   RETURNING id_item;""",
                                (item.nome, item.valor_base, item.classe_produto.tipo_produto, item.estabelecimento.id)
                                )
                    id_item = cur.fetchone()[0]
                    item.id = id_item
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_classificacao(self, classe_produto):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    if classe_produto.classificacao_pai:
                        cur.execute("SELECT 1 FROM classificacoes WHERE tipo_produto = %s", (classe_produto.classificacao_pai,))
                        busca = cur.fetchone()
                        if not busca:
                            raise ValueError(f"Erro: A classificação pai '{classe_produto.classificacao_pai}' não existe.")
                    cur.execute("""
                                INSERT INTO classificacoes (tipo_produto, classificacao_pai)
                                VALUES (%s, %s)
                                ;""", (classe_produto.tipo_produto, classe_produto.classificacao_pai)
                    )
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_classe_produto(self, classe_produto):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(""" SELECT tipo_produto, classificacao_pai FROM classificacoes
                                    WHERE tipo_produto = (%s)""", (classe_produto,))
                    resultado = cur.fetchone()
                    if not resultado:
                        print("Classe de produto não encontrada!")
                    else:
                        classe_produto = Classe_produto(resultado[0], resultado[1])
                        return classe_produto

                except Exception as e:
                    print(e)

    def buscar_item_por_id(self, id_item):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""SELECT id_item, nome, valor_base, classificacao, id_estabelecimento
                                    FROM itens WHERE id_item = (%s)""", (id_item,)
                    )
                    resultado = cur.fetchone()
                    if resultado:
                        estabelecimento_dao = EstabelecimentosDAO()
                        estabelecimento = estabelecimento_dao.buscar_estabelecimento_por_id(resultado[4])
                        classe_produto = self.buscar_classe_produto(resultado[3])
                        item = Item(resultado[0], resultado[1], resultado[2], classe_produto, estabelecimento)
                        return item
                    else:
                        print(f"Item não encontrado com id {id_item}!")

                except Exception as e:
                    print(e)