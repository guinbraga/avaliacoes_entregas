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

class_margherita = Classe_produto(tipo_produto="Margherita", classificacao_pai="Pizza")
class_queijos_4 = Classe_produto(tipo_produto="4 Queijos", classificacao_pai="Pizza")
class_frango_catupiry = Classe_produto(tipo_produto="Frango com Catupiry", classificacao_pai="Pizza")

item_dao = ItensDAO()

with get_db_connection() as conn:
    with conn.cursor() as cur:
        try:
            cur.execute(""" SELECT e.id_estabelecimento, e.cnpj, e.nome, e.endereco 
                            FROM estabelecimentos e JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
                            WHERE ce.id_categoria = 1""")

            resultado = cur.fetchall()
            for row in resultado:
                margherita = Item(id=None, nome="Margherita", valor_base=37.99, classe_produto_obj=class_margherita,
                                estabelecimento_obj=None)
                frango_catupiry = Item(id=None, nome="Frango com Catupiry", valor_base=41.99, classe_produto_obj=class_frango_catupiry,
                              estabelecimento_obj=None)
                queijos_4 = Item(id=None, nome="4 Queijos", valor_base=39.99, classe_produto_obj=class_queijos_4,
                               estabelecimento_obj=None)
                itens = [margherita, queijos_4, frango_catupiry]
                estabelecimento = Estabelecimento(row[0], row[1], row[2], row[3])
                for item in itens:
                    item.estabelecimento = estabelecimento
                    item_dao.inserir_item(item)

        except Exception as error:
            print(error)
            raise error


