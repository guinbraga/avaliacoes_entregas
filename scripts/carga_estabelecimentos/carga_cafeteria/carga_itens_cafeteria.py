# script para adicionar itens às hamburguerias do db
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.estabelecimentos import Estabelecimento
from app.models.itens import Item, Classe_produto
from app.dao.estabelecimentos_dao import EstabelecimentosDAO
from app.dao.itens_dao import ItensDAO
from app.dao.base import get_db_connection

estabelecimentos_dao = EstabelecimentosDAO()

# class_mocca = Classe_produto(tipo_produto="Mocca", classificacao_pai="Café")
class_expresso = Classe_produto(tipo_produto="Expresso", classificacao_pai="Café")
class_latte = Classe_produto(tipo_produto="Latte", classificacao_pai="Café")

item_dao = ItensDAO()

with get_db_connection() as conn:
    with conn.cursor() as cur:
        try:
            cur.execute(""" SELECT e.id_estabelecimento, e.cnpj, e.nome, e.endereco 
                            FROM estabelecimentos e JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
                            WHERE ce.id_categoria = 3""")

            resultado = cur.fetchall()
            for row in resultado:
                # mocca = Item(id=None, nome="Mocca", valor_base=12.99, classe_produto_obj=class_mocca,
                #                 estabelecimento_obj=None)
                latte = Item(id=None, nome="Latte", valor_base=11.99, classe_produto_obj=class_latte,
                              estabelecimento_obj=None)
                expresso = Item(id=None, nome="Expresso", valor_base=10.99, classe_produto_obj=class_expresso,
                               estabelecimento_obj=None)
                itens = [expresso, latte]
                estabelecimento = Estabelecimento(row[0], row[1], row[2], row[3])
                for item in itens:
                    item.estabelecimento = estabelecimento
                    item_dao.inserir_item(item)

        except Exception as error:
            print(error)
            raise error


