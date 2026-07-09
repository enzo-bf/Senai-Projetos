import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))

# Esconde o cursor padrão
pygame.mouse.set_visible(False)

raio = 20

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    x, y = pygame.mouse.get_pos()

    tela.fill((0, 0, 0))

    # Desenha apenas o seu cursor personalizado
    pygame.draw.circle(tela, (255, 0, 0), (x, y), raio)

    pygame.display.flip()

pygame.quit()