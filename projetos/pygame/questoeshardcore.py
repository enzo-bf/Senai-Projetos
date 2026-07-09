import pygame
import sys
import random

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Clique no Retângulo")

clock = pygame.time.Clock()

# Fonte para o texto
fonte = pygame.font.SysFont(None, 30)

# Personagem
x = 375
y = 275
tamanho = 50
velocidade = 5

# Cor inicial
cor_atual = (255, 255, 255)

rodando = True
while rodando:

    # Retângulo do personagem
    personagem = pygame.Rect(x, y, tamanho, tamanho)

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        # Detecta clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if personagem.collidepoint(evento.pos):
                cor_atual = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade

    tela.fill((0, 0, 0))

    pygame.draw.rect(tela, cor_atual, personagem)

    # Texto das coordenadas
    texto = fonte.render(f"X: {x}  Y: {y}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()