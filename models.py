from datetime import datetime, timezone

class Cliente:
    def __init__(self, id, cpf, endereco, sexo, nome):
        self.id = id
        self.cpf = cpf
        self.endereco = endereco
        self.sexo = sexo
        self.nome = nome

class Entregador:
    def __init__(self, id, cpf, nome):
        self.id = id
        self.cpf = cpf
        self.nome = nome

class Estabelecimento:
    def __init__(self, id, cnpj, nome, endereco):
        self.id = id
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco

class Classe_produto:
    def __init__(self, tipo_produto, classificacao_pai):
        self.tipo_produto = tipo_produto
        self.classificacao_pai = classificacao_pai

class Item:
    def __init__(self, id, nome, valor_base, classe_produto_obj, estabelecimento_obj):
        self.id = id
        self.nome = nome
        self.valor_base = valor_base
        self.classe_produto = classe_produto_obj
        self.estabelecimento = estabelecimento_obj

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

class Categoria:
    def __init__(self, id, categoria):
        self.id = id
        self.categoria = categoria

class Categoria_estabelecimento:
    def __init__(self, estabelecimento_obj, categoria_obj):
        self.estabelecimento = estabelecimento_obj
        self.categoria = categoria_obj

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
    def __init__(self, id, avaliacao_obj, questao_obj, item_pedido_obj, valor_resposta):
        self.id = id
        self.avaliacao = avaliacao_obj
        self.questao = questao_obj
        self.item_pedido = item_pedido_obj
        self.valor_resposta = valor_resposta
