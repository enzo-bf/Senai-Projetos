#Enzo de Barros Francisco
import pygame
import random
import wave
import struct
import math
import io
import os

pygame.init()

# =========================================================
# ÁUDIO (som de moeda gerado em memória, sem precisar de
# arquivos externos nem internet — só biblioteca padrão)
# =========================================================
SOM_ATIVADO = True
try:
    pygame.mixer.init()
except pygame.error:
    SOM_ATIVADO = False


def gerar_tom(frequencia, duracao, amplitude=0.5, taxa=44100):
    n_amostras = int(taxa * duracao)
    amostras = []
    for i in range(n_amostras):
        t = i / taxa
        fade = 1.0 - (i / n_amostras)  # evita "clique" no final do tom
        valor = amplitude * fade * math.sin(2 * math.pi * frequencia * t)
        amostras.append(int(valor * 32767))
    return amostras


def gerar_som_moeda():
    taxa = 44100
    tom1 = gerar_tom(988, 0.07, taxa=taxa)   # Si5
    tom2 = gerar_tom(1318, 0.12, taxa=taxa)  # Mi6
    amostras = tom1 + tom2

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(taxa)
        dados = struct.pack("<" + "h" * len(amostras), *amostras)
        wav_file.writeframes(dados)
    buffer.seek(0)
    return buffer


som_moeda = None
if SOM_ATIVADO:
    try:
        som_moeda = pygame.mixer.Sound(gerar_som_moeda())
    except Exception:
        SOM_ATIVADO = False


def tocar_som_moeda():
    if SOM_ATIVADO and som_moeda is not None:
        som_moeda.play()


# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================
LARGURA, ALTURA = 800, 600
PAINEL_LARGURA = 260
AREA_JOGO_LARGURA = LARGURA - PAINEL_LARGURA  # barreira: o quadrado não passa daqui

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Quadrado Fugitivo - Missões")
clock = pygame.time.Clock()

# =========================================================
# IMAGEM DO OVNI (usada quando o quadrado fica vermelho)
# O arquivo "ovni.png" deve estar na mesma pasta deste script.
# IMPORTANTE: o carregamento só pode acontecer DEPOIS que a janela
# (pygame.display.set_mode) já foi criada, senão o .convert_alpha() falha.
# =========================================================
CAMINHO_IMAGEM_OVNI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ovni.png")

imagem_ovni_original = None
try:
    imagem_ovni_original = pygame.image.load(CAMINHO_IMAGEM_OVNI).convert_alpha()
except (pygame.error, FileNotFoundError) as erro:
    imagem_ovni_original = None
    print(f"Aviso: não foi possível carregar 'ovni.png' ({erro}). "
          "Coloque o arquivo na mesma pasta do script para ativar a troca de imagem.")

# cache da imagem redimensionada, para não escalar a cada frame sem necessidade
_imagem_ovni_escalada = None
_ultimo_tamanho_escalado = None


def obter_imagem_ovni_escalada(tamanho):
    """Retorna a imagem do OVNI já escalada para o tamanho atual do alvo,
    reaproveitando o cache quando o tamanho não mudou."""
    global _imagem_ovni_escalada, _ultimo_tamanho_escalado

    if imagem_ovni_original is None:
        return None

    if _imagem_ovni_escalada is None or _ultimo_tamanho_escalado != tamanho:
        _imagem_ovni_escalada = pygame.transform.smoothscale(imagem_ovni_original, (tamanho, tamanho))
        _ultimo_tamanho_escalado = tamanho

    return _imagem_ovni_escalada


PRETO = (20, 20, 20)
PRETO_PAINEL = (25, 25, 30)
BRANCO = (255, 255, 255)
CINZA_LINHA = (80, 80, 90)
CINZA_BOTAO = (50, 50, 55)
VERDE = (40, 110, 40)
VERDE_TEXTO = (150, 255, 150)
VERMELHO = (220, 50, 50)
VERMELHO_CLARO = (255, 90, 90)
VERMELHO_GAMEOVER = (255, 40, 40)
AZUL = (50, 100, 255)
AZUL_CLARO = (90, 140, 255)
AMARELO = (230, 180, 40)
AMARELO_CLARO = (255, 210, 80)

fonte = pygame.font.SysFont("Arial", 30)
fonte_pop = pygame.font.SysFont("Arial", 24)
fonte_pop_titulo = pygame.font.SysFont("Arial", 28, bold=True)
fonte_titulo_jogo = pygame.font.SysFont("Arial", 50, bold=True)
fonte_menu_botao = pygame.font.SysFont("Arial", 28, bold=True)
fonte_gameover = pygame.font.SysFont("Arial", 70, bold=True)

# =========================================================
# CONFIGURAÇÕES DE DIFICULDADE
# =========================================================
DIFICULDADES = {
    "facil": {
        "nome": "Fácil",
        "tamanho_inicial": 80,
        "intervalo_missao": 10,
        "diminui_tamanho": False,
        "cor": VERDE,
        "cor_hover": (60, 150, 60),
    },
    "moderada": {
        "nome": "Moderada",
        "tamanho_inicial": 50,
        "intervalo_missao": 5,
        "diminui_tamanho": False,
        "cor": AZUL,
        "cor_hover": AZUL_CLARO,
    },
    "dificil": {
        "nome": "Difícil",
        "tamanho_inicial": 50,
        "intervalo_missao": 5,
        "diminui_tamanho": True,
        "cor": VERMELHO,
        "cor_hover": VERMELHO_CLARO,
    },
}

TAMANHO_MINIMO = 18
DIMINUICAO_TAMANHO = 6
INCREMENTO_VELOCIDADE = 1
NUM_MISSOES = 4
POPUP_DURACAO = 150  # ~2.5s a 60 FPS

# =========================================================
# FORMAS DO ALVO (botão "Mudar Forma")
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

forma_atual_index = 0


def pontos_poligono_regular(cx, cy, raio, lados, angulo_inicial=-90):
    """Gera os vértices de um polígono regular (pentágono, hexágono etc)."""
    pontos = []
    for i in range(lados):
        angulo = math.radians(angulo_inicial + i * (360 / lados))
        px = cx + raio * math.cos(angulo)
        py = cy + raio * math.sin(angulo)
        pontos.append((px, py))
    return pontos


def pontos_estrela(cx, cy, raio_externo, raio_interno, pontas=5, angulo_inicial=-90):
    """Gera os vértices de uma estrela de N pontas."""
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
        # fallback de segurança: nunca deve chegar aqui
        pygame.draw.rect(superficie, cor, rect)
        pygame.draw.rect(superficie, contorno, rect, 3)


def alternar_forma():
    """Avança para a próxima forma da lista, voltando ao início no final."""
    global forma_atual_index
    forma_atual_index = (forma_atual_index + 1) % len(FORMAS)

# =========================================================
# ESTADO DO JOGO
# =========================================================
ESTADO_MENU = "menu"
ESTADO_JOGO = "jogo"
ESTADO_GAMEOVER = "gameover"

estado = ESTADO_MENU
dificuldade_atual = None

tamanho_alvo = 50
x = y = 0
vel_x = vel_y = 5
cor_alvo = (255, 0, 0)
usar_imagem_ovni = False  # True quando o alvo está vermelho -> vira OVNI

pontos = 0
ultimo_marco_atingido = 0
meta_atual = 0  # meta da última missão concluída (usada para detectar o game over)
motivo_game_over = ""  # texto explicando por que o game over aconteceu
missoes = []

LIMITE_PONTOS_NEGATIVOS = -3  # game over automático ao atingir esse valor

popup_texto = ""
popup_timer = 0

# Botões do menu inicial
botao_facil = pygame.Rect(LARGURA // 2 - 140, 260, 280, 60)
botao_moderada = pygame.Rect(LARGURA // 2 - 140, 335, 280, 60)
botao_dificil = pygame.Rect(LARGURA // 2 - 140, 410, 280, 60)

# Botão de reset (posição fixa, dentro do painel de missões)
botao_reset = pygame.Rect(AREA_JOGO_LARGURA + 20, ALTURA - 70, PAINEL_LARGURA - 40, 45)

# Botão "Mudar Forma" (azul), logo acima do botão de reset
botao_mudar_forma = pygame.Rect(AREA_JOGO_LARGURA + 20, ALTURA - 130, PAINEL_LARGURA - 40, 45)

# Botão amarelo "Retornar ao Menu" (visível durante o jogo, dentro do painel)
botao_voltar_menu_jogo = pygame.Rect(AREA_JOGO_LARGURA + 20, ALTURA - 190, PAINEL_LARGURA - 40, 45)

# Botão "retornar ao menu" na tela de game over
botao_retornar_menu = pygame.Rect(LARGURA // 2 - 150, 420, 300, 60)


# =========================================================
# FUNÇÃO DE COR ALEATÓRIA
# =========================================================
CHANCE_DE_VERMELHO = 0.3  # chance de a cor sorteada ser um tom de vermelho


def cor_e_vermelha(cor):
    """Considera 'vermelho' um tom com R alto e G/B baixos (evita falsos
    positivos com laranja, rosa, roxo, etc.)."""
    r, g, b = cor
    return r > 180 and g < 90 and b < 90


def cor_aleatoria():
    # Garante uma chance real de sair vermelho, e evita que o sorteio
    # "normal" caia sem querer em um tom parecido com vermelho.
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
# FUNÇÕES DE CONTROLE DE JOGO
# =========================================================
def iniciar_jogo(dificuldade_chave):
    global estado, dificuldade_atual, tamanho_alvo, x, y, vel_x, vel_y
    global pontos, ultimo_marco_atingido, meta_atual, missoes, popup_timer, cor_alvo, usar_imagem_ovni
    global forma_atual_index, motivo_game_over

    dificuldade_atual = dificuldade_chave
    config = DIFICULDADES[dificuldade_chave]

    tamanho_alvo = config["tamanho_inicial"]
    x = AREA_JOGO_LARGURA // 2
    y = ALTURA // 2
    vel_x = 5
    vel_y = 5
    cor_alvo = (255, 0, 0)
    usar_imagem_ovni = cor_e_vermelha(cor_alvo)
    forma_atual_index = 0

    pontos = 0
    ultimo_marco_atingido = 0
    meta_atual = 0
    motivo_game_over = ""
    popup_timer = 0

    intervalo = config["intervalo_missao"]
    missoes = [
        {"meta": intervalo * i, "texto": f"Alcançar {intervalo * i} pontos", "concluida": False}
        for i in range(1, NUM_MISSOES + 1)
    ]

    estado = ESTADO_JOGO


def resetar_desafio():
    """Reseta o desafio do zero absoluto, sem voltar ao menu."""
    global tamanho_alvo, x, y, vel_x, vel_y, pontos
    global ultimo_marco_atingido, meta_atual, popup_timer, cor_alvo, usar_imagem_ovni, motivo_game_over

    config = DIFICULDADES[dificuldade_atual]
    tamanho_alvo = config["tamanho_inicial"]
    x = AREA_JOGO_LARGURA // 2
    y = ALTURA // 2
    vel_x = 5
    vel_y = 5
    cor_alvo = (255, 0, 0)
    usar_imagem_ovni = cor_e_vermelha(cor_alvo)
    pontos = 0
    ultimo_marco_atingido = 0
    meta_atual = 0
    motivo_game_over = ""
    popup_timer = 0

    for missao in missoes:
        missao["concluida"] = False


def voltar_ao_menu():
    global estado
    estado = ESTADO_MENU


def checar_missoes():
    global popup_texto, popup_timer, meta_atual
    for missao in missoes:
        if not missao["concluida"] and pontos >= missao["meta"]:
            missao["concluida"] = True
            meta_atual = missao["meta"]
            popup_texto = f"Missão concluída: {missao['texto']}!"
            popup_timer = POPUP_DURACAO


def checar_aumento_velocidade_e_tamanho():
    global ultimo_marco_atingido, vel_x, vel_y, tamanho_alvo, x, y

    config = DIFICULDADES[dificuldade_atual]
    intervalo = config["intervalo_missao"]
    marco_atual = pontos // intervalo

    if pontos > 0 and marco_atual > ultimo_marco_atingido:
        ultimo_marco_atingido = marco_atual

        sinal_x = 1 if vel_x >= 0 else -1
        sinal_y = 1 if vel_y >= 0 else -1
        vel_x = (abs(vel_x) + INCREMENTO_VELOCIDADE) * sinal_x
        vel_y = (abs(vel_y) + INCREMENTO_VELOCIDADE) * sinal_y

        if config["diminui_tamanho"]:
            centro_x = x + tamanho_alvo // 2
            centro_y = y + tamanho_alvo // 2
            tamanho_alvo = max(TAMANHO_MINIMO, tamanho_alvo - DIMINUICAO_TAMANHO)
            x = centro_x - tamanho_alvo // 2
            y = centro_y - tamanho_alvo // 2


def checar_game_over():
    """Game over acontece em dois casos:
    1) A pontuação caiu abaixo da última missão concluída.
    2) A pontuação atingiu o limite mínimo (LIMITE_PONTOS_NEGATIVOS)."""
    global estado, motivo_game_over

    if pontos <= LIMITE_PONTOS_NEGATIVOS:
        motivo_game_over = f"Você atingiu {LIMITE_PONTOS_NEGATIVOS} pontos (limite mínimo permitido)."
        estado = ESTADO_GAMEOVER
    elif meta_atual > 0 and pontos < meta_atual:
        motivo_game_over = f"Você caiu abaixo da meta de {meta_atual} pontos."
        estado = ESTADO_GAMEOVER


def registrar_acerto():
    """Chamado ao clicar DENTRO do alvo."""
    global pontos
    pontos += 1
    tocar_som_moeda()
    checar_aumento_velocidade_e_tamanho()
    checar_missoes()


def registrar_erro():
    """Chamado ao clicar FORA do alvo (mas dentro da área de jogo)."""
    global pontos
    pontos -= 1
    checar_game_over()


# =========================================================
# FUNÇÕES DE DESENHO
# =========================================================
def desenhar_botao(rect, cor, cor_hover, texto, fonte_usada):
    mouse_pos = pygame.mouse.get_pos()
    cor_final = cor_hover if rect.collidepoint(mouse_pos) else cor
    pygame.draw.rect(tela, cor_final, rect, border_radius=10)
    pygame.draw.rect(tela, (0, 0, 0), rect, 3, border_radius=10)
    txt = fonte_usada.render(texto, True, BRANCO)
    txt_rect = txt.get_rect(center=rect.center)
    tela.blit(txt, txt_rect)


def desenhar_menu():
    tela.fill((15, 15, 20))

    titulo = fonte_titulo_jogo.render("QUADRADO FUGITIVO", True, BRANCO)
    titulo_rect = titulo.get_rect(center=(LARGURA // 2, 110))
    tela.blit(titulo, titulo_rect)

    subtitulo = fonte_pop_titulo.render("Escolha a dificuldade", True, (200, 200, 200))
    subtitulo_rect = subtitulo.get_rect(center=(LARGURA // 2, 180))
    tela.blit(subtitulo, subtitulo_rect)

    desenhar_botao(botao_facil, DIFICULDADES["facil"]["cor"], DIFICULDADES["facil"]["cor_hover"],
                    "Fácil", fonte_menu_botao)
    desenhar_botao(botao_moderada, DIFICULDADES["moderada"]["cor"], DIFICULDADES["moderada"]["cor_hover"],
                    "Moderada", fonte_menu_botao)
    desenhar_botao(botao_dificil, DIFICULDADES["dificil"]["cor"], DIFICULDADES["dificil"]["cor_hover"],
                    "Difícil", fonte_menu_botao)

    dica1 = fonte_pop.render("Fácil: quadrado maior, missões a cada 10 pontos", True, (150, 150, 150))
    dica2 = fonte_pop.render("Moderada: tamanho normal, missões a cada 5 pontos", True, (150, 150, 150))
    dica3 = fonte_pop.render("Difícil: tamanho normal, diminui e acelera a cada 5 pontos", True, (150, 150, 150))
    tela.blit(dica1, dica1.get_rect(center=(LARGURA // 2, 500)))
    tela.blit(dica2, dica2.get_rect(center=(LARGURA // 2, 530)))
    tela.blit(dica3, dica3.get_rect(center=(LARGURA // 2, 560)))


def desenhar_painel_missoes():
    painel_x = AREA_JOGO_LARGURA
    painel = pygame.Surface((PAINEL_LARGURA, ALTURA))
    painel.fill(PRETO_PAINEL)
    tela.blit(painel, (painel_x, 0))

    pygame.draw.line(tela, CINZA_LINHA, (painel_x, 0), (painel_x, ALTURA), 3)

    titulo = fonte_pop_titulo.render("Missões", True, BRANCO)
    tela.blit(titulo, (painel_x + 20, 20))

    pygame.draw.line(tela, CINZA_LINHA, (painel_x + 20, 55), (LARGURA - 20, 55), 1)

    y_offset = 75
    for missao in missoes:
        cor_caixa = VERDE if missao["concluida"] else CINZA_BOTAO
        cor_texto = VERDE_TEXTO if missao["concluida"] else (220, 220, 220)
        simbolo = "OK" if missao["concluida"] else "o"

        caixa = pygame.Rect(painel_x + 15, y_offset, PAINEL_LARGURA - 30, 40)
        pygame.draw.rect(tela, cor_caixa, caixa, border_radius=8)
        pygame.draw.rect(tela, (0, 0, 0), caixa, 2, border_radius=8)

        texto_missao = fonte_pop.render(f"{simbolo}  {missao['texto']}", True, cor_texto)
        tela.blit(texto_missao, (caixa.x + 10, caixa.y + 8))

        y_offset += 55

    desenhar_botao(botao_voltar_menu_jogo, AMARELO, AMARELO_CLARO, "Retornar ao Menu", fonte_pop)
    desenhar_botao(botao_mudar_forma, AZUL, AZUL_CLARO, "Mudar Forma", fonte_pop)
    desenhar_botao(botao_reset, VERMELHO, VERMELHO_CLARO, "RESET", fonte_pop)


def desenhar_popup():
    if popup_timer > 0:
        largura_caixa = 460
        altura_caixa = 70
        caixa_x = (AREA_JOGO_LARGURA - largura_caixa) // 2
        caixa_y = 30

        caixa = pygame.Rect(caixa_x, caixa_y, largura_caixa, altura_caixa)

        superficie = pygame.Surface((largura_caixa, altura_caixa))
        superficie.set_alpha(230)
        superficie.fill(VERDE)
        tela.blit(superficie, (caixa_x, caixa_y))

        pygame.draw.rect(tela, (0, 0, 0), caixa, 3, border_radius=10)

        texto_render = fonte_pop_titulo.render(popup_texto, True, BRANCO)
        texto_rect = texto_render.get_rect(center=caixa.center)
        tela.blit(texto_render, texto_rect)


def desenhar_jogo():
    tela.fill(PRETO)

    if usar_imagem_ovni:
        imagem = obter_imagem_ovni_escalada(tamanho_alvo)
        tela.blit(imagem, (x, y))
    else:
        alvo_rect = pygame.Rect(x, y, tamanho_alvo, tamanho_alvo)
        desenhar_forma(tela, FORMAS[forma_atual_index], alvo_rect, cor_alvo)

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    texto_vel = fonte_pop.render(f"Velocidade: {abs(vel_x)}", True, (200, 200, 200))
    tela.blit(texto_vel, (10, 50))

    texto_dif = fonte_pop.render(f"Dificuldade: {DIFICULDADES[dificuldade_atual]['nome']}", True, (200, 200, 200))
    tela.blit(texto_dif, (10, 80))

    texto_forma = fonte_pop.render(f"Forma: {NOMES_FORMAS[FORMAS[forma_atual_index]]}", True, (200, 200, 200))
    tela.blit(texto_forma, (10, 110))

    if meta_atual > 0:
        texto_meta = fonte_pop.render(f"Não caia abaixo de {meta_atual} pontos!", True, (255, 200, 100))
        tela.blit(texto_meta, (10, 140))

    desenhar_painel_missoes()
    desenhar_popup()


def desenhar_game_over():
    tela.fill((10, 10, 10))

    texto_go = fonte_gameover.render("GAME OVER", True, VERMELHO_GAMEOVER)
    texto_rect = texto_go.get_rect(center=(LARGURA // 2, 220))
    tela.blit(texto_go, texto_rect)

    subtexto = fonte_pop_titulo.render(motivo_game_over, True, (220, 220, 220))
    subtexto_rect = subtexto.get_rect(center=(LARGURA // 2, 300))
    tela.blit(subtexto, subtexto_rect)

    pontuacao_final = fonte_pop.render(f"Pontuação final: {pontos}", True, (200, 200, 200))
    pontuacao_rect = pontuacao_final.get_rect(center=(LARGURA // 2, 340))
    tela.blit(pontuacao_final, pontuacao_rect)

    desenhar_botao(botao_retornar_menu, AMARELO, AMARELO_CLARO, "Retornar ao Menu", fonte_menu_botao)


# =========================================================
# LOOP PRINCIPAL
# =========================================================
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = evento.pos

            if estado == ESTADO_MENU:
                if botao_facil.collidepoint(evento.pos):
                    iniciar_jogo("facil")
                elif botao_moderada.collidepoint(evento.pos):
                    iniciar_jogo("moderada")
                elif botao_dificil.collidepoint(evento.pos):
                    iniciar_jogo("dificil")

            elif estado == ESTADO_JOGO:
                if botao_reset.collidepoint(evento.pos):
                    resetar_desafio()
                elif botao_mudar_forma.collidepoint(evento.pos):
                    alternar_forma()
                elif botao_voltar_menu_jogo.collidepoint(evento.pos):
                    voltar_ao_menu()
                else:
                    alvo_rect = pygame.Rect(x, y, tamanho_alvo, tamanho_alvo)

                    if alvo_rect.collidepoint(evento.pos):
                        registrar_acerto()
                    elif mx < AREA_JOGO_LARGURA:
                        registrar_erro()

            elif estado == ESTADO_GAMEOVER:
                if botao_retornar_menu.collidepoint(evento.pos):
                    voltar_ao_menu()

    # ---------------- LÓGICA ----------------
    if estado == ESTADO_JOGO:
        x += vel_x
        y += vel_y

        bateu_na_parede = False

        # Barreira: o quadrado não ultrapassa a área de missões
        if x <= 0 or x + tamanho_alvo >= AREA_JOGO_LARGURA:
            vel_x *= -1
            x = max(0, min(x, AREA_JOGO_LARGURA - tamanho_alvo))
            bateu_na_parede = True

        if y <= 0 or y + tamanho_alvo >= ALTURA:
            vel_y *= -1
            y = max(0, min(y, ALTURA - tamanho_alvo))
            bateu_na_parede = True

        if bateu_na_parede:
            cor_alvo = cor_aleatoria()
            # Só vira OVNI se a nova cor for vermelha; qualquer outra cor
            # diferente de vermelho faz o alvo voltar a ser um quadrado.
            usar_imagem_ovni = cor_e_vermelha(cor_alvo) and imagem_ovni_original is not None

        if popup_timer > 0:
            popup_timer -= 1

    # ---------------- DESENHO ----------------
    if estado == ESTADO_MENU:
        desenhar_menu()
    elif estado == ESTADO_JOGO:
        desenhar_jogo()
    elif estado == ESTADO_GAMEOVER:
        desenhar_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
