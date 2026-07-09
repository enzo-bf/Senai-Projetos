import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Botão Esquerdo e Direito")

# Cor inicial do círculo
cor = (0, 0, 0)  # Preto

# Loop principal
rodando = True
while rodando:

    for evento in pygame.event.get():

        # Fechar a janela
        if evento.type == pygame.QUIT:
            rodando = False

        # Clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            # Botão esquerdo
            if evento.button == 1:
                cor = (255, 0, 0)  # Vermelho

            # Botão direito
            if evento.button == 3:
                cor = (0, 0, 255)  # Azul

    # Obtém a posição do mouse
    x, y = pygame.mouse.get_pos()

    # Limpa a tela
    tela.fill((0, 0, 0))

    # Desenha o círculo
    pygame.draw.circle(tela, cor, (x, y), 20)

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()