from personagem import Personagem

def test_usar_pocao_recupera_vida_e_consome_item():
    heroi = Personagem ("Aria")
    heroi.vida = 50
    heroi.inventario.adicionar("poção de vida", 2)

    heroi.usar_pocao()

    assert heroi.vida == 80
    assert heroi.inventario.itens["poção de vida"] == 1