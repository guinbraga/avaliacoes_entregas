# script para adicionar pizzarias ao db
from faker import Faker
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.estabelecimentos import Estabelecimento, Categoria_estabelecimento, Categoria
from app.models.itens import Item
from app.dao.estabelecimentos_dao import EstabelecimentosDAO
from app.dao.itens_dao import ItensDAO

fake = Faker("pt_BR")
estabelecimentos_dao = EstabelecimentosDAO()

with open("pizzaria_nomes.txt") as f:
    for line in f:
        nome = line.strip()
        cnpj = fake.company_id()
        endereco = fake.street_address()
        categoria = 'Pizzaria'

        estabelecimento_obj = Estabelecimento(id=None, nome=nome, cnpj=cnpj, endereco=endereco)

        try:
            estabelecimentos_dao.inserir_estabelecimento(estabelecimento_obj)

            if estabelecimento_obj.id:
                categoria_obj = Categoria(id=1, categoria=categoria)
                categoria_estabelecimento = Categoria_estabelecimento(estabelecimento_obj, categoria_obj)
                estabelecimentos_dao.inserir_categoria_estabelecimento(categoria_estabelecimento)
            else:
                print(f"Falha ao inserir {nome}: ID não gerado.")

        except Exception as e:
            print(f"Pulei o estabelecimento {nome} devido a erro: {e}")