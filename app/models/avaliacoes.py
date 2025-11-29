class Pergunta:
    def __init__(self, id, enunciado_pergunta, tipo_resposta, alvo_avaliacao):
        self.id = id
        self.enunciado_pergunta = enunciado_pergunta
        self.tipo_resposta = tipo_resposta
        self.alvo_avaliacao = alvo_avaliacao

class Avaliacao:
    def __init__(self, id, data_hora, pedido_obj):
        self.id = id
        self.data_hora = data_hora
        self.pedido = pedido_obj

class Resposta:
    def __init__(self, id, avaliacao_obj, pergunta_obj, item_pedido_obj, valor_resposta):
        self.id = id
        self.avaliacao = avaliacao_obj
        self.pergunta = pergunta_obj
        self.item_pedido = item_pedido_obj
        self.valor_resposta = valor_resposta