import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mira Telescópica")

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Obtém a posição atual do mouse
    x, y = pygame.mouse.get_pos()

    tela.fill((0, 0, 0))

    # Linha horizontal
    pygame.draw.line(tela, (255, 0, 0), (0, y), (largura, y), 2)

    # Linha vertical
    pygame.draw.line(tela, (255, 0, 0), (x, 0), (x, altura), 2)

    pygame.display.flip()

pygame.quit()