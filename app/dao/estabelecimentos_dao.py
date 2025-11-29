from app.models import Estabelecimento
from .base import get_db_connection

class EstabelecimentosDAO:
    def inserir_estabelecimento(self, estabelecimento):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO estabelecimentos (nome, cnpj, endereco)
                                values (%s, %s, %s)
                                RETURNING id_estabelecimento;""",
                                (estabelecimento.nome, estabelecimento.cnpj, estabelecimento.endereco)
                                )
                    id_estabelecimento = cur.fetchone()[0]
                    estabelecimento.id = id_estabelecimento
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_categoria(self, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""INSERT INTO categorias (categoria) VALUES (%s)
                                   RETURNING id_categoria;
                                """, (categoria.categoria,)
                    )
                    id_categoria = cur.fetchone()[0]
                    categoria.id = id_categoria
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def inserir_categoria_estabelecimento(self, categoria_estabelecimento):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
               try:
                   cur.execute("""INSERT INTO categorias_estabelecimento (id_estabelecimento, id_categoria)
                                  VALUES (%s, %s);""",
                                  (categoria_estabelecimento.estabelecimento.id, categoria_estabelecimento.categoria.id)
                               )
                   conn.commit()
               except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_estabelecimento_por_id(self, id_estabelecimento):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT id_estabelecimento, cnpj, nome, endereco
                                FROM estabelecimentos
                                WHERE id_estabelecimento = (%s)
                                """, (id_estabelecimento,)
                                )

                    resultado = cur.fetchone()
                    if resultado:
                        estabelecimento_obj = Estabelecimento(resultado[0], resultado[1], resultado[2], resultado[3])
                        return estabelecimento_obj

                    else:
                        print(f"Nenhum estabelecimento encontrado com id {id_estabelecimento}")
                        return None

                except Exception as e:
                    print(e)
                    return None

    def buscar_estabelecimentos_por_categoria(self, categoria):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT e.id_estabelecimento, e.cnpj, e.nome, e.endereco
                                FROM estabelecimentos e 
                                JOIN categorias_estabelecimento ce ON e.id_estabelecimento = ce.id_estabelecimento
                                WHERE ce.id_categoria = (SELECT id_categoria FROM categorias
                                                    WHERE categoria = (%s))
                                """, (categoria,))
                    resultado = cur.fetchall()
                    if not resultado:
                        print(f"Nenhum estabelecimento encontrado com categoria {categoria}")
                    estabelecimentos = []
                    for item in resultado:
                        estabelecimento = Estabelecimento(item[0], item[1], item[2], item[3])
                        estabelecimentos.append(estabelecimento)

                    return estabelecimentos
                except Exception as e:
                    print(e)
                    return None

