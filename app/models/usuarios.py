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
