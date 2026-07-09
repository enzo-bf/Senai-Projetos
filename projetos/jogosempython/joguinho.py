import pygame
import random

# Inicialização
pygame.init()

# Configurações da janela
LARGURA = 900
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong - Tênis de Mesa")

# Cores
PRETO = (20, 20, 20)
BRANCO = (255, 255, 255)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Fonte
fonte = pygame.font.SysFont("Arial", 50)

# Raquetes
LARG_RAQUETE = 15
ALT_RAQUETE = 120
VEL_RAQUETE = 8

raquete_esq = pygame.Rect(
    30,
    ALTURA // 2 - ALT_RAQUETE // 2,
    LARG_RAQUETE,
    ALT_RAQUETE,
)

raquete_dir = pygame.Rect(
    LARGURA - 45,
    ALTURA // 2 - ALT_RAQUETE // 2,
    LARG_RAQUETE,
    ALT_RAQUETE,
)

# Bola
TAM_BOLA = 18
bola = pygame.Rect(
    LARGURA // 2 - TAM_BOLA // 2,
    ALTURA // 2 - TAM_BOLA // 2,
    TAM_BOLA,
    TAM_BOLA,
)

vel_x = random.choice([-6, 6])
vel_y = random.choice([-4, 4])

# Placar
placar_esq = 0
placar_dir = 0


def reiniciar_bola():
    global vel_x, vel_y

    bola.center = (LARGURA // 2, ALTURA // 2)

    vel_x = random.choice([-6, 6])
    vel_y = random.randint(-4, 4)

    if vel_y == 0:
        vel_y = random.choice([-3, 3])


rodando = True

while rodando:

    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Controles
    teclas = pygame.key.get_pressed()

    # Jogador esquerdo (W/S)
    if teclas[pygame.K_w] and raquete_esq.top > 0:
        raquete_esq.y -= VEL_RAQUETE
    if teclas[pygame.K_s] and raquete_esq.bottom < ALTURA:
        raquete_esq.y += VEL_RAQUETE

    # Jogador direito (Setas)
    if teclas[pygame.K_UP] and raquete_dir.top > 0:
        raquete_dir.y -= VEL_RAQUETE
    if teclas[pygame.K_DOWN] and raquete_dir.bottom < ALTURA:
        raquete_dir.y += VEL_RAQUETE

    # Movimento da bola
    bola.x += vel_x
    bola.y += vel_y

    # Colisão com topo e base
    if bola.top <= 0 or bola.bottom >= ALTURA:
        vel_y *= -1

    # Colisão com raquetes
    if bola.colliderect(raquete_esq):
        vel_x *= -1
        bola.left = raquete_esq.right

    if bola.colliderect(raquete_dir):
        vel_x *= -1
        bola.right = raquete_dir.left

    # Pontuação
    if bola.left <= 0:
        placar_dir += 1
        reiniciar_bola()

    if bola.right >= LARGURA:
        placar_esq += 1
        reiniciar_bola()

    # Desenho
    TELA.fill(PRETO)

    # Linha central
    pygame.draw.aaline(
        TELA,
        BRANCO,
        (LARGURA // 2, 0),
        (LARGURA // 2, ALTURA),
    )

    # Raquetes
    pygame.draw.rect(TELA, BRANCO, raquete_esq)
    pygame.draw.rect(TELA, BRANCO, raquete_dir)

    # Bola
    pygame.draw.ellipse(TELA, BRANCO, bola)

    # Placar
    texto = fonte.render(f"{placar_esq}     {placar_dir}", True, BRANCO)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 20))

    pygame.display.flip()

pygame.quit()