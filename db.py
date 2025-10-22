import psycopg
import sys

DB_URL = "postgresql://postgres:Guilhormo%40123@localhost/imeals"

def get_db_connection():
    """ Cria e retorna uma nova conexão com o banco de dados """
    try:
        connection = psycopg.connect(DB_URL)
        return connection
    except Exception as e:
        print(f"Erro: não foi possível conectar ao banco de dados: {e}")
        sys.exit(1)

