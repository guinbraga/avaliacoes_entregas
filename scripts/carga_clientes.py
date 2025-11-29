from faker import Faker
import sys
import os
import random
from datetime import datetime
from random_carga_faker import criar_clientes_aleatorios, criar_entregadores_aleatorios

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao.base import get_db_connection

with get_db_connection() as conn:
    criar_clientes_aleatorios(conn, 400)
    criar_entregadores_aleatorios(conn, 80)