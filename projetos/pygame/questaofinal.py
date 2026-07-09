import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Exercícios de Mouse")

# Cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Cor inicial
cor = VERMELHO

# Raio inicial do círculo
raio = 20

# Exercício 4 - Esconde o cursor padrão
pygame.mouse.set_visible(False)

rodando = True

while rodando:

    for evento in pygame.event.get():

        # Fechar a janela
        if evento.type == pygame.QUIT:
            rodando = False

        # Exercícios 5 e 6 - Botões do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            # Botão esquerdo -> Vermelho
            if evento.button == 1:
                cor = VERMELHO

            # Botão direito -> Azul
            elif evento.button == 3:
                cor = AZUL

            # Exercício 2 - Scroll para cima
            elif evento.button == 4:
                raio += 5

            # Exercício 2 - Scroll para baixo
            elif evento.button == 5:
                raio -= 5

                if raio < 5:
                    raio = 5

    # Posição do mouse
    x, y = pygame.mouse.get_pos()

    # Exercício 1
    # A linha abaixo foi comentada para criar o efeito de rastro
    # tela.fill(PRETO)

    # Exercício 3 - Mira telescópica
    pygame.draw.line(tela, cor, (0, y), (LARGURA, y), 1)
    pygame.draw.line(tela, cor, (x, 0), (x, ALTURA), 1)

    # Círculo que acompanha o mouse
    pygame.draw.circle(tela, cor, (x, y), raio)

    pygame.display.flip()

pygame.quit()