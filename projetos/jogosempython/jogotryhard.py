import pygame
import random

# 1. Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Exercício 1: Movimentação Básica")

# Cores
PRETO = (0, 0, 0)
cor_quadrado = (0, 255, 0)

# 2. Variáveis do Jogador
tamanho_quadrado = 100

pos_x = LARGURA // 2
pos_y = ALTURA // 2
velocidade = 30

relogio = pygame.time.Clock()
rodando = True

# Controle para evitar aumentar/diminuir várias vezes enquanto segura a tecla
w_pressionado = False
s_pressionado = False

# --- LOOP PRINCIPAL ---
while rodando:

    # A. Tratamento de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # B. Captura de Teclas Pressionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        pos_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        pos_x += velocidade
    if teclas[pygame.K_UP]:
        pos_y -= velocidade
    if teclas[pygame.K_DOWN]:
        pos_y += velocidade

    # Aumenta o tamanho com W
    if teclas[pygame.K_w]:
        if not w_pressionado:
            tamanho_quadrado += 10
            w_pressionado = True
    else:
        w_pressionado = False

    # Diminui o tamanho com S
    if teclas[pygame.K_s]:
        if not s_pressionado:
            tamanho_quadrado -= 10
            if tamanho_quadrado < 20:
                tamanho_quadrado = 20
            s_pressionado = True
    else:
        s_pressionado = False

    # C. Lógica Pac-Man + Mudança de cor
    mudou_cor = False

    if pos_x > LARGURA:
        pos_x = -tamanho_quadrado
        mudou_cor = True

    if pos_x + tamanho_quadrado < 0:
        pos_x = LARGURA
        mudou_cor = True

    if pos_y > ALTURA:
        pos_y = -tamanho_quadrado
        mudou_cor = True

    if pos_y + tamanho_quadrado < 0:
        pos_y = ALTURA
        mudou_cor = True

    # Se atravessou uma borda, sorteia uma nova cor
    if mudou_cor:
        cor_quadrado = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    # D. Desenho (Renderização)
    tela.fill(PRETO)

    pygame.draw.rect(
        tela,
        cor_quadrado,
        (pos_x, pos_y, tamanho_quadrado, tamanho_quadrado)
    )

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()