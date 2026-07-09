class Inventario:
    def __init__(self):
        self.itens = {}
    def adicionar (self, item, quantidade = 1):
        self.itens[item] = self.itens.get(item,0) + quantidade
    def remover (self, item, quantidade = 1):
        if self.itens.get(item, 0)< quantidade:
            raise ValueError ("quantidade insuficiente")
        self.item [item] -= quantidade