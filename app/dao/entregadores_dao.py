from app.models import Entregador
from .base import get_db_connection

class EntregadoresDAO:
    def inserir_entregador(self, entregador):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO entregadores (nome, cpf)
                                VALUES (%s, %s)
                                RETURNING id_entregador;
                                """,
                                (entregador.nome, entregador.cpf)
                                )
                    id_entregador = cur.fetchone()[0]
                    entregador.id = id_entregador
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_entregador_por_id(self, id_entregador):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                    SELECT id_entregador, cpf, nome FROM entregadores
                                        WHERE id_entregador = (%s)
                                        """, (id_entregador,)
                    )

                    resultado = cur.fetchone()
                    if resultado:
                        entregador_obj = Entregador(resultado[0], resultado[1], resultado[2])
                        return entregador_obj

                    else:
                        print(f"Nenhum entregador encontrado com id {id_entregador}")
                        return None

                except Exception as e:
                    print(e)
                    return None

    def buscar_entregadores_todos(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(""" SELECT * FROM entregadores""")
                    resultado = cur.fetchall()
                    if not resultado:
                        print(f"Nenhum entregador encontrado")
                    entregadores = []
                    for item in resultado:
                        entregador = Entregador(item[0], item[1], item[2])
                        entregadores.append(entregador)
                    return entregadores
                except Exception as e:
                    print(e)