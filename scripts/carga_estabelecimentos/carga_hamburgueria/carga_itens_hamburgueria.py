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

class_x_salada = Classe_produto(tipo_produto="X-Salada", classificacao_pai="Hambúrguer")
class_x_bacon = Classe_produto(tipo_produto="X-Bacon", classificacao_pai="Hambúrguer")
class_x_tudo = Classe_produto(tipo_produto="X-Tudo", classificacao_pai="Hambúrguer")

item_dao = ItensDAO()

with get_db_connection() as conn:
    with conn.cursor() as cur:
        try:
            cur.execute(""" SELECT e.id_estabelecimento, e.cnpj, e.nome, e.endereco 
                            FROM estabelecimentos e JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
                            WHERE ce.id_categoria = 2""")

            resultado = cur.fetchall()
            for row in resultado:
                x_salada = Item(id=None, nome="X-Salada", valor_base=15.99, classe_produto_obj=class_x_salada,
                                estabelecimento_obj=None)
                x_tudo = Item(id=None, nome="X-Tudo", valor_base=19.99, classe_produto_obj=class_x_tudo,
                              estabelecimento_obj=None)
                x_bacon = Item(id=None, nome="X-Bacon", valor_base=17.99, classe_produto_obj=class_x_bacon,
                               estabelecimento_obj=None)
                itens = [x_salada, x_bacon, x_tudo]
                estabelecimento = Estabelecimento(row[0], row[1], row[2], row[3])
                for item in itens:
                    item.estabelecimento = estabelecimento
                    item_dao.inserir_item(item)

        except Exception as error:
            print(error)
            raise error


