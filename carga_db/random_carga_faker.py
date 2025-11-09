from faker import Faker
import random
import psycopg
from acesso_db import get_db_connection


def criar_clientes_aleatorios(conn, n_clientes):
    """ Cria n_clientes aleatórios usando uma conexão pré-existente

    NÃO commita a transação.
    """
    fake = Faker('pt_BR')
    sexo_valores = ['M', 'F']
    clientes_criados = 0

    cur = conn.cursor()

    try:
        for _ in range(n_clientes):
            cpf = fake.ssn()
            endereco = fake.street_address()
            sexo = sexo_valores[random.randint(0,1)]
            nome = f"{fake.first_name()} {fake.last_name()}"
            cur.execute("""
                INSERT INTO clientes (cpf, endereco, sexo, nome) VALUES (%s, %s, %s, %s);
                """,
                (cpf, endereco, sexo, nome)
            )
            clientes_criados += 1

    except Exception as e:
        print(f"Erro ao criar cliente: {e}")
        raise e

    finally:
        print(f"Total de clientes criados: {clientes_criados}")
        cur.close()

def criar_entregadores_aleatorios(conn, n_entregadores):
    """ Cria n_entregadores aleatórios usando uma conexão pré-existente

    NÃO commita a transação.
    """
    fake = Faker('pt_BR')
    entregadores_criados = 0

    cur = conn.cursor()

    try:
        for _ in range(n_entregadores):
            cpf = fake.ssn()
            nome = f"{fake.first_name()} {fake.last_name()}"
            cur.execute("""
                INSERT INTO entregadores (nome, cpf) VALUES (%s, %s);
                """,
                (nome, cpf)
            )
            entregadores_criados += 1

    except Exception as e:
        print(f"Erro ao criar entregador: {e}")
        raise e

    finally:
        print(f"Total de entregadores criados: {entregadores_criados}")
        cur.close()

def criar_categoria_estabelecimento(categoria, conn):
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO categorias (categoria) VALUES (%s);
            """, (categoria,)
        )

    except Exception as e:
        print(f"Erro ao criar categoria: {e}")
        raise e

    finally:
        cur.close()


def criar_estabelecimento(cnpj, nome, conn):
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO estabelecimentos (cnpj, nome) VALUES (%s, %s);
            """, (cnpj, nome)
        )

    except Exception as e:
        print(f"Erro ao criar estabelecimento: {e}")
        raise e
    finally:
        cur.close()

