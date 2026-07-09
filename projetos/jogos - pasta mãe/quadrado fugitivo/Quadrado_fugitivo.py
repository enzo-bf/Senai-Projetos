#Enzo de Barros Francisco
import pygame
import random
import math
import os

pygame.init()

# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================
LARGURA_JOGO = 800
ALTURA = 600
LARGURA_PAINEL = 220
LARGURA_TOTAL = LARGURA_JOGO + LARGURA_PAINEL

tela = pygame.display.set_mode((LARGURA_TOTAL, ALTURA))
pygame.display.set_caption("Quadrado Fugitivo")
clock = pygame.time.Clock()

# =========================================================
# IMAGEM DO OVNI (usada quando o quadrado fica vermelho)
# O arquivo "ovni.png" precisa estar na mesma pasta deste script.
# IMPORTANTE: o carregamento só pode acontecer DEPOIS da criação da
# janela (pygame.display.set_mode), senão o .convert_alpha() falha.
# =========================================================
CAMINHO_IMAGEM_OVNI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ovni.png")

imagem_ovni_original = None
try:
    imagem_ovni_original = pygame.image.load(CAMINHO_IMAGEM_OVNI).convert_alpha()
except (pygame.error, FileNotFoundError) as erro:
    imagem_ovni_original = None
    print(f"Aviso: não foi possível carregar 'ovni.png' ({erro}). "
          "Coloque o arquivo na mesma pasta do script para ativar a troca de imagem.")

_imagem_ovni_escalada = None
_ultimo_tamanho_escalado = None


def obter_imagem_ovni_escalada(tamanho):
    global _imagem_ovni_escalada, _ultimo_tamanho_escalado

    if imagem_ovni_original is None:
        return None

    if _imagem_ovni_escalada is None or _ultimo_tamanho_escalado != tamanho:
        _imagem_ovni_escalada = pygame.transform.smoothscale(imagem_ovni_original, (tamanho, tamanho))
        _ultimo_tamanho_escalado = tamanho

    return _imagem_ovni_escalada


# =========================================================
# CORES
# =========================================================
PRETO = (20, 20, 20)
PRETO_PAINEL = (25, 25, 30)
BRANCO = (255, 255, 255)
CINZA_LINHA = (80, 80, 90)
VERMELHO = (220, 50, 50)
VERMELHO_CLARO = (255, 90, 90)
AZUL = (50, 100, 255)
AZUL_CLARO = (90, 140, 255)

fonte = pygame.font.SysFont("Arial", 26)
fonte_titulo = pygame.font.SysFont("Arial", 30, bold=True)
fonte_titulo_painel = pygame.font.SysFont("Arial", 24, bold=True)
fonte_botao = pygame.font.SysFont("Arial", 22)

# =========================================================
# FORMAS DO QUADRADO (botão "Mudar Forma")
# =========================================================
FORMAS = [
    "quadrado",
    "circulo",
    "triangulo",
    "triangulo_invertido",
    "losango",
    "pentagono",
    "hexagono",
    "estrela",
    "cruz",
    "seta",
    "trapezio",
]

NOMES_FORMAS = {
    "quadrado": "Quadrado",
    "circulo": "Círculo",
    "triangulo": "Triângulo",
    "triangulo_invertido": "Triângulo Invertido",
    "losango": "Losango",
    "pentagono": "Pentágono",
    "hexagono": "Hexágono",
    "estrela": "Estrela",
    "cruz": "Cruz",
    "seta": "Seta",
    "trapezio": "Trapézio",
}


def pontos_poligono_regular(cx, cy, raio, lados, angulo_inicial=-90):
    pontos = []
    for i in range(lados):
        angulo = math.radians(angulo_inicial + i * (360 / lados))
        px = cx + raio * math.cos(angulo)
        py = cy + raio * math.sin(angulo)
        pontos.append((px, py))
    return pontos


def pontos_estrela(cx, cy, raio_externo, raio_interno, pontas=5, angulo_inicial=-90):
    pontos = []
    passo = 360 / (pontas * 2)
    for i in range(pontas * 2):
        raio = raio_externo if i % 2 == 0 else raio_interno
        angulo = math.radians(angulo_inicial + i * passo)
        px = cx + raio * math.cos(angulo)
        py = cy + raio * math.sin(angulo)
        pontos.append((px, py))
    return pontos


def desenhar_forma(superficie, forma, rect, cor):
    """Desenha a forma geométrica atual dentro do retângulo (hitbox) do alvo."""
    cx, cy = rect.center
    w, h = rect.width, rect.height
    raio = min(w, h) // 2
    contorno = (0, 0, 0)

    if forma == "quadrado":
        pygame.draw.rect(superficie, cor, rect)
        pygame.draw.rect(superficie, contorno, rect, 3)

    elif forma == "circulo":
        pygame.draw.circle(superficie, cor, (cx, cy), raio)
        pygame.draw.circle(superficie, contorno, (cx, cy), raio, 3)

    elif forma == "triangulo":
        pontos = [(cx, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom)]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "triangulo_invertido":
        pontos = [(rect.left, rect.top), (rect.right, rect.top), (cx, rect.bottom)]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "losango":
        pontos = [(cx, rect.top), (rect.right, cy), (cx, rect.bottom), (rect.left, cy)]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "pentagono":
        pontos = pontos_poligono_regular(cx, cy, raio, 5)
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "hexagono":
        pontos = pontos_poligono_regular(cx, cy, raio, 6)
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "estrela":
        pontos = pontos_estrela(cx, cy, raio, raio * 0.45, pontas=5)
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "cruz":
        espessura = max(6, w // 3)
        rect_v = pygame.Rect(cx - espessura // 2, rect.top, espessura, h)
        rect_h = pygame.Rect(rect.left, cy - espessura // 2, w, espessura)
        pygame.draw.rect(superficie, cor, rect_v)
        pygame.draw.rect(superficie, cor, rect_h)
        pygame.draw.rect(superficie, contorno, rect_v, 2)
        pygame.draw.rect(superficie, contorno, rect_h, 2)

    elif forma == "seta":
        faixa = h // 4
        pontos = [
            (rect.left, cy - faixa),
            (cx, cy - faixa),
            (cx, rect.top),
            (rect.right, cy),
            (cx, rect.bottom),
            (cx, cy + faixa),
            (rect.left, cy + faixa),
        ]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    elif forma == "trapezio":
        recuo = w // 4
        pontos = [
            (rect.left + recuo, rect.top),
            (rect.right - recuo, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom),
        ]
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, contorno, pontos, 3)

    else:
        pygame.draw.rect(superficie, cor, rect)
        pygame.draw.rect(superficie, contorno, rect, 3)


forma_atual_index = 0


def alternar_forma():
    global forma_atual_index
    forma_atual_index = (forma_atual_index + 1) % len(FORMAS)


# =========================================================
# COR ALEATÓRIA (com detecção de vermelho)
# =========================================================
CHANCE_DE_VERMELHO = 0.3


def cor_e_vermelha(cor):
    r, g, b = cor
    return r > 180 and g < 90 and b < 90


def cor_aleatoria():
    if random.random() < CHANCE_DE_VERMELHO:
        return (random.randint(200, 255), random.randint(0, 60), random.randint(0, 60))

    while True:
        cor = (
            random.randint(60, 255),
            random.randint(60, 255),
            random.randint(60, 255),
        )
        if not cor_e_vermelha(cor):
            return cor


# =========================================================
# ESTADO DO QUADRADO
# =========================================================
TAMANHO_INICIAL = 50
VELOCIDADE_INICIAL = 5

tamanho = TAMANHO_INICIAL
velocidade = VELOCIDADE_INICIAL
cor_atual = (255, 255, 255)
usar_imagem_ovni = False
estava_na_borda = False


def posicao_central():
    return LARGURA_JOGO // 2 - tamanho // 2, ALTURA // 2 - tamanho // 2


x, y = posicao_central()


def resetar():
    """Volta o quadrado para o centro, com velocidade e forma iniciais."""
    global x, y, tamanho, velocidade, cor_atual, usar_imagem_ovni, forma_atual_index, estava_na_borda
    tamanho = TAMANHO_INICIAL
    velocidade = VELOCIDADE_INICIAL
    x, y = posicao_central()
    cor_atual = (255, 255, 255)
    usar_imagem_ovni = False
    forma_atual_index = 0
    estava_na_borda = False


# =========================================================
# BOTÕES DO PAINEL LATERAL
# =========================================================
PADDING = 20
LARGURA_BOTAO = LARGURA_PAINEL - PADDING * 2

botao_aumentar_velocidade = pygame.Rect(LARGURA_JOGO + PADDING, 120, LARGURA_BOTAO, 50)
botao_mudar_forma = pygame.Rect(LARGURA_JOGO + PADDING, 190, LARGURA_BOTAO, 50)
botao_reset = pygame.Rect(LARGURA_JOGO + PADDING, 280, LARGURA_BOTAO, 50)


def desenhar_botao(rect, cor, cor_hover, texto):
    mouse_pos = pygame.mouse.get_pos()
    cor_final = cor_hover if rect.collidepoint(mouse_pos) else cor
    pygame.draw.rect(tela, cor_final, rect, border_radius=10)
    pygame.draw.rect(tela, (0, 0, 0), rect, 3, border_radius=10)
    txt = fonte_botao.render(texto, True, BRANCO)
    txt_rect = txt.get_rect(center=rect.center)
    tela.blit(txt, txt_rect)


def texto_centralizado_painel(texto, fonte_usada, cor, y_pos):
    surf = fonte_usada.render(texto, True, cor)
    rect = surf.get_rect(centerx=LARGURA_JOGO + LARGURA_PAINEL // 2, y=y_pos)
    tela.blit(surf, rect)


def desenhar_painel():
    painel_x = LARGURA_JOGO
    pygame.draw.rect(tela, PRETO_PAINEL, (painel_x, 0, LARGURA_PAINEL, ALTURA))
    pygame.draw.line(tela, CINZA_LINHA, (painel_x, 0), (painel_x, ALTURA), 3)

    texto_centralizado_painel("Menu de", fonte_titulo_painel, BRANCO, 15)
    texto_centralizado_painel("Controle", fonte_titulo_painel, BRANCO, 45)
    pygame.draw.line(tela, CINZA_LINHA, (painel_x + PADDING, 85), (LARGURA_TOTAL - PADDING, 85), 1)

    desenhar_botao(botao_aumentar_velocidade, AZUL, AZUL_CLARO, "Aumentar Velocidade")
    desenhar_botao(botao_mudar_forma, AZUL, AZUL_CLARO, "Mudar Forma")
    desenhar_botao(botao_reset, VERMELHO, VERMELHO_CLARO, "RESET")

    pygame.draw.line(tela, CINZA_LINHA, (painel_x + PADDING, 350), (LARGURA_TOTAL - PADDING, 350), 1)

    texto_centralizado_painel("Status", fonte_botao, (180, 180, 180), 365)
    texto_centralizado_painel(f"Velocidade: {velocidade}", fonte_botao, BRANCO, 400)
    texto_centralizado_painel(f"Forma: {NOMES_FORMAS[FORMAS[forma_atual_index]]}", fonte_botao, BRANCO, 430)


# =========================================================
# LOOP PRINCIPAL
# =========================================================
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_aumentar_velocidade.collidepoint(evento.pos):
                velocidade += 1
            elif botao_mudar_forma.collidepoint(evento.pos):
                alternar_forma()
            elif botao_reset.collidepoint(evento.pos):
                resetar()

    # ---------------- MOVIMENTO (setas do teclado) ----------------
    teclas = pygame.key.get_pressed()
    dx = dy = 0
    if teclas[pygame.K_LEFT]:
        dx -= 1
    if teclas[pygame.K_RIGHT]:
        dx += 1
    if teclas[pygame.K_UP]:
        dy -= 1
    if teclas[pygame.K_DOWN]:
        dy += 1

    nova_x = x + dx * velocidade
    nova_y = y + dy * velocidade

    limite_x = max(0, min(nova_x, LARGURA_JOGO - tamanho))
    limite_y = max(0, min(nova_y, ALTURA - tamanho))

    bateu_na_borda = (limite_x != nova_x) or (limite_y != nova_y)

    if bateu_na_borda and not estava_na_borda:
        cor_atual = cor_aleatoria()
        usar_imagem_ovni = cor_e_vermelha(cor_atual) and imagem_ovni_original is not None

    estava_na_borda = bateu_na_borda
    x, y = limite_x, limite_y

    # ---------------- DESENHO ----------------
    tela.fill(PRETO)

    if usar_imagem_ovni:
        imagem = obter_imagem_ovni_escalada(tamanho)
        tela.blit(imagem, (x, y))
    else:
        alvo_rect = pygame.Rect(x, y, tamanho, tamanho)
        desenhar_forma(tela, FORMAS[forma_atual_index], alvo_rect, cor_atual)

    texto_coord = fonte.render(f"X: {x}   Y: {y}", True, BRANCO)
    fundo_coord = pygame.Rect(5, 5, texto_coord.get_width() + 10, texto_coord.get_height() + 6)
    pygame.draw.rect(tela, (0, 0, 0), fundo_coord)
    pygame.draw.rect(tela, CINZA_LINHA, fundo_coord, 1)
    tela.blit(texto_coord, (10, 8))

    desenhar_painel()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
