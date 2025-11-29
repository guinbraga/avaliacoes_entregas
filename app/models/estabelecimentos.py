class Estabelecimento:
    def __init__(self, id, cnpj, nome, endereco):
        self.id = id
        self.cnpj = cnpj
        self.nome = nome
        self.endereco = endereco

class Categoria:
    def __init__(self, id, categoria):
        self.id = id
        self.categoria = categoria

class Categoria_estabelecimento:
    def __init__(self, estabelecimento_obj, categoria_obj):
        self.estabelecimento = estabelecimento_obj
        self.categoria = categoria_obj