#Enzo de Barros Francisco
import pygame
import random
import wave
import struct
import math
import io

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
pygame.display.set_caption("Caça ao Alvo - Missões")
clock = pygame.time.Clock()

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

pontos = 0
ultimo_marco_atingido = 0
meta_atual = 0  # meta da última missão concluída (usada para detectar o game over)
missoes = []

popup_texto = ""
popup_timer = 0

# Botões do menu inicial
botao_facil = pygame.Rect(LARGURA // 2 - 140, 260, 280, 60)
botao_moderada = pygame.Rect(LARGURA // 2 - 140, 335, 280, 60)
botao_dificil = pygame.Rect(LARGURA // 2 - 140, 410, 280, 60)

# Botão de reset (posição fixa, dentro do painel de missões)
botao_reset = pygame.Rect(AREA_JOGO_LARGURA + 20, ALTURA - 70, PAINEL_LARGURA - 40, 45)

# Botão "retornar ao menu" na tela de game over
botao_retornar_menu = pygame.Rect(LARGURA // 2 - 150, 420, 300, 60)


# =========================================================
# FUNÇÃO DE COR ALEATÓRIA
# =========================================================
def cor_aleatoria():
    return (
        random.randint(60, 255),
        random.randint(60, 255),
        random.randint(60, 255),
    )


# =========================================================
# FUNÇÕES DE CONTROLE DE JOGO
# =========================================================
def iniciar_jogo(dificuldade_chave):
    global estado, dificuldade_atual, tamanho_alvo, x, y, vel_x, vel_y
    global pontos, ultimo_marco_atingido, meta_atual, missoes, popup_timer, cor_alvo

    dificuldade_atual = dificuldade_chave
    config = DIFICULDADES[dificuldade_chave]

    tamanho_alvo = config["tamanho_inicial"]
    x = AREA_JOGO_LARGURA // 2
    y = ALTURA // 2
    vel_x = 5
    vel_y = 5
    cor_alvo = (255, 0, 0)

    pontos = 0
    ultimo_marco_atingido = 0
    meta_atual = 0
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
    global ultimo_marco_atingido, meta_atual, popup_timer, cor_alvo

    config = DIFICULDADES[dificuldade_atual]
    tamanho_alvo = config["tamanho_inicial"]
    x = AREA_JOGO_LARGURA // 2
    y = ALTURA // 2
    vel_x = 5
    vel_y = 5
    cor_alvo = (255, 0, 0)
    pontos = 0
    ultimo_marco_atingido = 0
    meta_atual = 0
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
    """Game over: a pontuação caiu abaixo da última missão concluída."""
    global estado
    if meta_atual > 0 and pontos < meta_atual:
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

    titulo = fonte_titulo_jogo.render("CAÇA AO ALVO", True, BRANCO)
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
    pygame.draw.rect(tela, cor_alvo, (x, y, tamanho_alvo, tamanho_alvo))
    pygame.draw.rect(tela, (0, 0, 0), (x, y, tamanho_alvo, tamanho_alvo), 3)

    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    texto_vel = fonte_pop.render(f"Velocidade: {abs(vel_x)}", True, (200, 200, 200))
    tela.blit(texto_vel, (10, 50))

    texto_dif = fonte_pop.render(f"Dificuldade: {DIFICULDADES[dificuldade_atual]['nome']}", True, (200, 200, 200))
    tela.blit(texto_dif, (10, 80))

    if meta_atual > 0:
        texto_meta = fonte_pop.render(f"Não caia abaixo de {meta_atual} pontos!", True, (255, 200, 100))
        tela.blit(texto_meta, (10, 110))

    desenhar_painel_missoes()
    desenhar_popup()


def desenhar_game_over():
    tela.fill((10, 10, 10))

    texto_go = fonte_gameover.render("GAME OVER", True, VERMELHO_GAMEOVER)
    texto_rect = texto_go.get_rect(center=(LARGURA // 2, 220))
    tela.blit(texto_go, texto_rect)

    subtexto = fonte_pop_titulo.render(
        f"Você caiu abaixo da meta de {meta_atual} pontos", True, (220, 220, 220)
    )
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
