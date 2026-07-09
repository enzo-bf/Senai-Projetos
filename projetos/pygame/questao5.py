import pygame

# Inicializa o Pygame
pygame.init()

# Cria a janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Botão Direito vs. Esquerdo")

# Cor inicial (preto)
cor = (0, 0, 0)

rodando = True

while rodando:
    for evento in pygame.event.get():

        # Fechar a janela
        if evento.type == pygame.QUIT:
            rodando = False

        # Detecta clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            # Botão esquerdo → Vermelho
            if evento.button == 1:
                cor = (255, 0, 0)

            # Botão direito → Azul
            elif evento.button == 3:
                cor = (0, 0, 255)

    # Obtém a posição do mouse
    x, y = pygame.mouse.get_pos()

    # Limpa a tela
    tela.fill((0, 0, 0))

    # Desenha um círculo na posição do mouse
    pygame.draw.circle(tela, cor, (x, y), 20)

    # Atualiza a tela
    pygame.display.flip()

# Encerra o Pygame
pygame.quit()