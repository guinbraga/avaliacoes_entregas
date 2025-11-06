# script rodado para adicionar categorias ao db
# NÁO RODAR NOVAMENTE
from random_carga_faker import criar_categoria_estabelecimento
from db import get_db_connection

conn = get_db_connection()
curr = conn.cursor()
curr.execute("""
                ALTER TABLE categorias ADD CONSTRAINT unique_categoria UNIQUE (categoria)
                    """)

criar_categoria_estabelecimento("Pizzaria", conn)
criar_categoria_estabelecimento("Hamburgueria", conn)
criar_categoria_estabelecimento("Cafeteria", conn)

conn.commit()