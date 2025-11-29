from datetime import datetime, timezone

class Pedido:
    def __init__(self, id, estabelecimento_obj, cliente_obj, status, entregador_obj, data_hora=datetime.now(timezone.utc)):
        self.id = id
        self.estabelecimento = estabelecimento_obj
        self.cliente = cliente_obj
        self.data_hora = data_hora
        self.status = status
        self.entregador = entregador_obj

class Item_pedido:
    def __init__(self, id, pedido_obj, item_obj, quantidade, preco_unidade):
        self.id = id
        self.pedido = pedido_obj
        self.item = item_obj
        self.quantidade = quantidade
        self.preco_unidade = preco_unidade