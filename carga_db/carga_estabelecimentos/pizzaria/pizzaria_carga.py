# SCRIPT QUE ADICIONA ALGUMAS PIZZARIAS AO BD
from acesso_db import get_db_connection
from faker import Faker

# Adicionei a constraint de unique nome para não termos problemas caso o script seja rodado novamente>
conn = get_db_connection()
cur = conn.cursor()
cur.execute("ALTER TABLE estabelecimentos ADD CONSTRAINT unique_nome UNIQUE(nome)")
conn.commit()

fake = Faker("pt_BR")

with open("cafeteria_nomes.txt") as f:
    for line in f:
        nome = line.strip()
        cnpj = fake.company_id()
        endereco = fake.street_address()
        categoria = 'Pizzaria'

        cur = conn.cursor()
        cur.execute("""
                INSERT INTO estabelecimentos (nome, cnpj, endereco) values (%s, %s, %s)
                    """, (nome, cnpj, endereco)
        )
    conn.commit()