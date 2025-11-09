# SCRIPT QUE ADICIONA ALGUMAS CAFETERIAS AO BD
# NÃO RODAR NOVAMENTE!
from acesso_db import get_db_connection
from faker import Faker

# Adicionei a constraint de unique nome para não termos problemas caso o script seja rodado novamente>
# cur.execute("ALTER TABLE estabelecimentos ADD CONSTRAINT unique_nome UNIQUE(nome)")
# conn.commit()

fake = Faker("pt_BR")

with open("cafeteria_nomes.txt") as f:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            try:
                for line in f:
                    nome = line.strip()
                    cnpj = fake.company_id()
                    endereco = fake.street_address()
                    categoria = 'Cafeteria'

                    cur.execute("""
                            INSERT INTO estabelecimentos (nome, cnpj, endereco) 
                            values (%s, %s, %s)
                            RETURNING id_estabelecimento;""", (nome, cnpj, endereco)
                    )

                    id_estabelecimento = cur.fetchone()[0]

                    cur.execute("""SELECT id_categoria FROM categorias WHERE categoria = (%s);""", (categoria,))
                    id_categoria = cur.fetchone()[0]

                    cur.execute("""INSERT INTO categorias_estabelecimento (id_estabelecimento, id_categoria)
                        VALUES (%s, %s);""", (id_estabelecimento, id_categoria)
                    )

                    conn.commit()
            except Exception as e:
                print(e)
