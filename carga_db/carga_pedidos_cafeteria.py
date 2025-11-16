import random
from acesso_db import DBManager
from models import Estabelecimento, Pedido, Item_pedido
from datetime import datetime, timezone

db = DBManager()
estabelecimentos = db.buscar_estabelecimentos_por_categoria("Cafeteria")
print(len(estabelecimentos))
clientes = db.buscar_clientes()
entregadores = db.buscar_entregadores()
for _ in range(7):
    estabelecimento = random.choice(estabelecimentos)
    cliente = random.choice(clientes)
    entregador = random.choice(entregadores)
    mocca = db.buscar_mocca_por_estabelecimento(estabelecimento)
    pedido = Pedido(None,
                    estabelecimento,
                    cliente,
                    "Concluído",
                    entregador,
                    datetime.now(timezone.utc)
                    )
    itens_pedido = []
    item = Item_pedido(None, pedido, mocca, 3, mocca.valor_base)
    itens_pedido.append(item)
    db.inserir_pedido(pedido, itens_pedido)