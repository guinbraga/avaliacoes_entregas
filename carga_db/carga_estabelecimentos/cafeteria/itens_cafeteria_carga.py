from acesso_db import DBManager, get_db_connection
from models import Estabelecimento, Item, Classe_produto
db = DBManager()

moca_classe = Classe_produto('Mocca', 'Café')
moca = Item(None, "Mocca", 12.99, moca_classe, None)
# pegando todos os ids de estabelecimento para adicionar Moca ao item vendido.

with get_db_connection() as conn:
    with conn.cursor() as cur:
        try:
            cur.execute("""
                            SELECT id_estabelecimento FROM estabelecimentos;
            """)
            resultado = cur.fetchall()
            for id in resultado:
                estabelecimento = db.buscar_estabelecimento_por_id(id[0])
                moca = Item(None, "Mocca", 12.99, moca_classe, estabelecimento)
                db.inserir_item(moca)


        except Exception as e:
            print(e)
