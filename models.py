class Cliente:
    def __init__(self, id, cpf, endereco, genero, nome):
        self.id = id
        self.cpf = cpf
        self.endereco = endereco
        self.genero = genero
        self.nome = nome

class Entregador:
    def __init__(self, id, cpf, nome):
        self.id = id
        self.cpf = cpf
        self.nome = nome

class Estabelecimento:
    def __init__(self, id, cnpj, nome):
        self.id = id
        self.cnpj = cnpj
        self.nome = nome

class Classe_produto:
    def __init__(self, tipo_produto, classificacao_pai):
        self.tipo_produto = tipo_produto
        self.classificacao_pai = classificacao_pai

class Item:
    def __init__(self, id, nome, valor_base, classe_produto, id_estabelecimento):
        self.id = id
        self.nome = nome
        self.valor_base = valor_base
        self.classe_produto = classe_produto
        self.id_estabelecimento = id_estabelecimento

class Pedido:
    def __init__(self, id, id_estabelecimento, id_cliente, data_hora, status, id_entregador):
        self.id = id
        self.id_estabelecimento = id_estabelecimento
        self.id_cliente = id_cliente
        self.data_hora = data_hora
        self.status = status
        self.id_entregador = id_entregador

class Item_pedido:
    def __init__(self, id, id_item_pedido, id_pedido, id_item, quantidade, preco_unidade):
        self.id = id
        self.id_item_pedido = id_item_pedido
        self.id_pedido = id_pedido
        self.id_item = id_item
        self.quantidade = quantidade
        self.preco_unidade = preco_unidade

class Categoria:
    def __init__(self, id, categoria):
        self.id = id
        self.categoria = categoria

class Categoria_estabelecimento:
    def __init__(self, id_estabelecimento, id_categoria):
        self.id_estabelecimento = id_estabelecimento
        self.id_categoria = id_categoria

class Pergunta:
    def __init__(self, id, enunciado_pergunta, tipo_resposta, alvo_avaliacao):
        self.id = id
        self.enunciado_pergunta = enunciado_pergunta
        self.tipo_resposta = tipo_resposta
        self.alvo_avaliacao = alvo_avaliacao

class Avaliacao:
    def __init__(self, id, data_hora, id_pedido):
        self.id = id
        self.data_hora = data_hora
        self.id_pedido = id_pedido

class Resposta:
    def __init__(self, id, id_avaliacao, id_questao, id_item_pedido, valor_resposta):
        self.id = id
        self.id_avaliacao = id_avaliacao
        self.id_questao = id_questao
        self.id_item_pedido = id_item_pedido
        self.valor_resposta = valor_resposta
