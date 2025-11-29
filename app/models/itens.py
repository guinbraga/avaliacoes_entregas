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