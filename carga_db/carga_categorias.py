# script rodado para adicionar categorias ao db
# NÁO RODAR NOVAMENTE
from acesso_db import DBManager

# conn = get_db_connection()
# curr = conn.cursor()
# curr.execute("""
#                 ALTER TABLE categorias ADD CONSTRAINT unique_categoria UNIQUE (categoria)
#                     """)
db_manager = DBManager()
db_manager.inserir_categoria('Pizzaria')
db_manager.inserir_categoria('Cafeteria')
db_manager.inserir_categoria('Hamburgueria')