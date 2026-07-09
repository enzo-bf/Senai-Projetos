from inventario import Inventario

class Personagem:
    def __init__(self, nome):
        self.nome = nome
        self.vida = 100
        self.inventario = Inventario()
    def usar_pocao(self):
        self.inventario.remover("poção de vida")
        self.vida = min (100, self.vida, 30)