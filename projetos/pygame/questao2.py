import pygame

pygame.init()

largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))

raio = 50

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Scroll para cima
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:
                raio += 5

            # Scroll para baixo
            elif evento.button == 5:
                raio -= 5

                # Evita que o raio fique negativo
                if raio < 1:
                    raio = 1

    tela.fill((0, 0, 0))

    pygame.draw.circle(tela, (0, 0, 255), (largura // 2, altura // 2), raio)

    pygame.display.flip()

pygame.quit()