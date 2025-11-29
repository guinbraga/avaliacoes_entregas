import psycopg

DB_URL = "postgresql://postgres:Guilhormo%40123@localhost/imeals"

def get_db_connection():
    try:
        return psycopg.connect(DB_URL)
    except Exception as e:
        print(f"Erro conexão: {e}")
        return None