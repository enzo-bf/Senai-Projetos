import pygame
import sys
import random
import math

pygame.init()

LARGURA_JOGO = 800
ALTURA = 600
LARGURA_MENU = 220
LARGURA = LARGURA_JOGO + LARGURA_MENU

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA_ESCURO = (30, 30, 35)
CINZA_LINHA = (60, 60, 65)
AZUL = (50, 100, 255)
AZUL_CLARO = (90, 140, 255)
VERMELHO = (220, 50, 50)
VERMELHO_CLARO = (255, 90, 90)
CINZA_TEXTO = (180, 180, 180)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadrado com Rastro e Menu")

clock = pygame.time.Clock()
fonte_titulo = pygame.font.SysFont(None, 34)
fonte = pygame.font.SysFont(None, 26)
fonte_botao = pygame.font.SysFont(None, 22)
fonte_coord = pygame.font.SysFont(None, 28)


def posicao_central():
    return LARGURA_JOGO // 2, ALTURA // 2


x, y = posicao_central()
prev_x, prev_y = x, y
tamanho = 50
velocidade = 5
cor_atual = BRANCO
ESPESSURA_CONTORNO = 3

area_jogo = pygame.Surface((LARGURA_JOGO, ALTURA))
area_jogo.fill(PRETO)

MENU_X = LARGURA_JOGO
PADDING = 25
LARGURA_BOTAO = LARGURA_MENU - (PADDING * 2)

botao_aum_vel = pygame.Rect(MENU_X + PADDING, 130, LARGURA_BOTAO, 45)
botao_dim_vel = pygame.Rect(MENU_X + PADDING, 185, LARGURA_BOTAO, 45)
botao_aum_tam = pygame.Rect(MENU_X + PADDING, 250, LARGURA_BOTAO, 45)
botao_dim_tam = pygame.Rect(MENU_X + PADDING, 305, LARGURA_BOTAO, 45)
botao_reset = pygame.Rect(MENU_X + PADDING, 415, LARGURA_BOTAO, 50)


def desenhar_botao(rect, cor, cor_hover, texto):
    mouse_pos = pygame.mouse.get_pos()
    cor_final = cor_hover if rect.collidepoint(mouse_pos) else cor
    pygame.draw.rect(tela, cor_final, rect, border_radius=10)
    pygame.draw.rect(tela, PRETO, rect, 2, border_radius=10)
    txt = fonte_botao.render(texto, True, BRANCO)
    txt_rect = txt.get_rect(center=rect.center)
    tela.blit(txt, txt_rect)


def texto_centralizado(texto, fonte_usada, cor, y_pos):
    surf = fonte_usada.render(texto, True, cor)
    rect = surf.get_rect(centerx=MENU_X + LARGURA_MENU // 2, y=y_pos)
    tela.blit(surf, rect)


def desenhar_rastro(superficie, p1, p2, tam, cor):
    """Desenha uma trilha arredondada entre dois pontos, usando círculos
    interpolados, evitando o aspecto de 'quinas' nas curvas."""
    raio = tam // 2
    centro1 = (p1[0] + raio, p1[1] + raio)
    centro2 = (p2[0] + raio, p2[1] + raio)

    distancia = math.hypot(centro2[0] - centro1[0], centro2[1] - centro1[1])
    passos = max(1, int(distancia))

    for i in range(passos + 1):
        t = i / passos
        cx = centro1[0] + (centro2[0] - centro1[0]) * t
        cy = centro1[1] + (centro2[1] - centro1[1]) * t
        pygame.draw.circle(superficie, cor, (int(cx), int(cy)), raio)


rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos

            if botao_aum_vel.collidepoint(evento.pos):
                velocidade += 2

            elif botao_dim_vel.collidepoint(evento.pos):
                velocidade = max(1, velocidade - 2)

            elif botao_aum_tam.collidepoint(evento.pos):
                tamanho += 10

            elif botao_dim_tam.collidepoint(evento.pos):
                tamanho = max(10, tamanho - 10)

            elif botao_reset.collidepoint(evento.pos):
                x, y = posicao_central()
                prev_x, prev_y = x, y
                area_jogo.fill(PRETO)

            elif mx < LARGURA_JOGO:
                cor_atual = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )

    prev_x, prev_y = x, y

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade

    x = max(0, min(x, LARGURA_JOGO - tamanho))
    y = max(0, min(y, ALTURA - tamanho))

    personagem = pygame.Rect(x, y, tamanho, tamanho)

    # Rastro: trilha arredondada interpolada entre a posição anterior e a atual
    desenhar_rastro(area_jogo, (prev_x, prev_y), (x, y), tamanho, cor_atual)

    tela.blit(area_jogo, (0, 0))

    # Contorno do quadrado atual (não persiste no rastro)
    pygame.draw.rect(tela, PRETO, personagem, ESPESSURA_CONTORNO)

    # --- Painel do menu ---
    pygame.draw.rect(tela, CINZA_ESCURO, (LARGURA_JOGO, 0, LARGURA_MENU, ALTURA))
    pygame.draw.line(tela, CINZA_LINHA, (LARGURA_JOGO, 0), (LARGURA_JOGO, ALTURA), 2)

    texto_centralizado("MENU", fonte_titulo, BRANCO, 35)
    pygame.draw.line(tela, CINZA_LINHA, (MENU_X + PADDING, 75), (LARGURA - PADDING, 75), 1)

    texto_centralizado("Controles", fonte, CINZA_TEXTO, 95)
    desenhar_botao(botao_aum_vel, AZUL, AZUL_CLARO, "Aumentar Velocidade")
    desenhar_botao(botao_dim_vel, AZUL, AZUL_CLARO, "Diminuir Velocidade")
    desenhar_botao(botao_aum_tam, AZUL, AZUL_CLARO, "Aumentar Tamanho")
    desenhar_botao(botao_dim_tam, AZUL, AZUL_CLARO, "Diminuir Tamanho")

    pygame.draw.line(tela, CINZA_LINHA, (MENU_X + PADDING, 380), (LARGURA - PADDING, 380), 1)

    texto_centralizado("Ações", fonte, CINZA_TEXTO, 395)
    desenhar_botao(botao_reset, VERMELHO, VERMELHO_CLARO, "RESET")

    pygame.draw.line(tela, CINZA_LINHA, (MENU_X + PADDING, 500), (LARGURA - PADDING, 500), 1)

    texto_centralizado("Status", fonte, CINZA_TEXTO, 515)
    texto_centralizado(f"Velocidade: {velocidade}", fonte_botao, BRANCO, 550)
    texto_centralizado(f"Tamanho: {tamanho}", fonte_botao, BRANCO, 580)

    texto_coord = fonte_coord.render(f"X: {x}   Y: {y}", True, BRANCO)
    fundo_coord = pygame.Rect(5, 5, texto_coord.get_width() + 10, texto_coord.get_height() + 6)
    pygame.draw.rect(tela, (0, 0, 0), fundo_coord)
    pygame.draw.rect(tela, CINZA_LINHA, fundo_coord, 1)
    tela.blit(texto_coord, (10, 8))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()