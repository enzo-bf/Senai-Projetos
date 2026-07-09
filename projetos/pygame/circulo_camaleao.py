#Enzo de Barros Francisco
import pygame
import sys

pygame.init()

LARGURA = 800
ALTURA = 600

PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mira Telescópica")

clock = pygame.time.Clock()

cor_atual = VERMELHO
raio = 20

pygame.mouse.set_visible(False)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                cor_atual = VERMELHO
            elif evento.button == 3:
                cor_atual = AZUL
            elif evento.button == pygame.BUTTON_WHEELUP:
                raio += 2
            elif evento.button == pygame.BUTTON_WHEELDOWN:
                raio = max(2, raio - 2)

    mx, my = pygame.mouse.get_pos()

    #tela.fill(PRETO)

    # Linha horizontal atravessando a tela inteira
    pygame.draw.line(tela, cor_atual, (0, my), (LARGURA, my), 2)

    # Linha vertical atravessando a tela inteira
    pygame.draw.line(tela, cor_atual, (mx, 0), (mx, ALTURA), 2)

    # Bola (círculo) na posição do mouse, no cruzamento das linhas
    pygame.draw.circle(tela, cor_atual, (mx, my), raio)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()