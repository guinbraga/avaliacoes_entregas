from .base import get_db_connection
from ..models import Cliente

class ClientesDAO:
    def inserir_cliente(self, cliente):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                INSERT INTO clientes (cpf, endereco, sexo, nome)
                                VALUES (%s, %s, %s, %s)
                                RETURNING id_cliente;
                                """,
                                (cliente.cpf, cliente.endereco, cliente.sexo, cliente.nome)
                                )
                    id_cliente = cur.fetchone()[0]
                    cliente.id = id_cliente
                    conn.commit()
                except Exception as e:
                    print(e)
                    conn.rollback()

    def buscar_cliente_por_id(self, id_cliente):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT id_cliente, cpf, endereco, sexo, nome
                                FROM clientes
                                WHERE id_cliente = (%s)
                                """, (id_cliente,)
                                )

                    resultado = cur.fetchone()
                    if resultado:
                        cliente_obj = Cliente(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4])
                        return cliente_obj

                    else:
                        print(f"Nenhum cliente encontrado com id {id_cliente}")
                        return None

                except Exception as e:
                    print(e)
                    return None

    def buscar_clientes_todos(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(""" SELECT * FROM clientes""")
                    resultado = cur.fetchall()
                    if not resultado:
                        print(f"Nenhum cliente encontrado")
                    clientes = []
                    for item in resultado:
                        cliente = Cliente(item[0], item[1], item[2], item[3], item[4])
                        clientes.append(cliente)
                    return clientes
                except Exception as e:
                    print(e)