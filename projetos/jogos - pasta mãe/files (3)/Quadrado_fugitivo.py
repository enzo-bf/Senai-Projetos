import pygame
import random
import math
import os

pygame.init()

# =========================================================
# CONFIGURAÇÕES GERAIS (sem painel/menu lateral)
# =========================================================
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
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
BRANCO = (255, 255, 255)
CINZA_LINHA = (80, 80, 90)
CINZA_TEXTO = (170, 170, 170)

fonte = pygame.font.SysFont("Arial", 26)
fonte_pequena = pygame.font.SysFont("Arial", 20)

# =========================================================
# FORMAS DO QUADRADO (tecla M)
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
    return LARGURA // 2 - tamanho // 2, ALTURA // 2 - tamanho // 2


x, y = posicao_central()


def aumentar_velocidade():
    global velocidade
    velocidade += 1


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
# LOOP PRINCIPAL
# =========================================================
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            # Sem menu de botões: os comandos agora são feitos pelo teclado
            if evento.key == pygame.K_SPACE:
                aumentar_velocidade()
            elif evento.key == pygame.K_m:
                alternar_forma()
            elif evento.key == pygame.K_r:
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

    limite_x = max(0, min(nova_x, LARGURA - tamanho))
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

    # Coordenadas (canto superior esquerdo)
    texto_coord = fonte.render(f"X: {x}   Y: {y}", True, BRANCO)
    fundo_coord = pygame.Rect(5, 5, texto_coord.get_width() + 10, texto_coord.get_height() + 6)
    pygame.draw.rect(tela, (0, 0, 0), fundo_coord)
    pygame.draw.rect(tela, CINZA_LINHA, fundo_coord, 1)
    tela.blit(texto_coord, (10, 8))

    # Velocidade e forma atuais (canto superior esquerdo, abaixo das coordenadas)
    texto_vel = fonte_pequena.render(f"Velocidade: {velocidade}", True, CINZA_TEXTO)
    tela.blit(texto_vel, (10, 45))

    texto_forma = fonte_pequena.render(f"Forma: {NOMES_FORMAS[FORMAS[forma_atual_index]]}", True, CINZA_TEXTO)
    tela.blit(texto_forma, (10, 70))

    # Instruções de teclado (canto inferior esquerdo, já que não há mais menu)
    instrucoes = [
        "Setas: mover",
        "ESPAÇO: aumentar velocidade",
        "M: mudar forma",
        "R: reset",
    ]
    y_instrucao = ALTURA - (len(instrucoes) * 24) - 10
    for linha in instrucoes:
        texto_instrucao = fonte_pequena.render(linha, True, CINZA_TEXTO)
        tela.blit(texto_instrucao, (10, y_instrucao))
        y_instrucao += 24

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
