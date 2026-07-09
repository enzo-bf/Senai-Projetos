import pygame

# 1. Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 1000, 1000
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Exercício 1: Movimentação Básica")

# Cores (RGB)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# 2. Variáveis do Jogador
tamanho_quadrado = 100

pos_x = LARGURA // 2  # Começa no meio da largura
pos_y = ALTURA // 2   # Começa no meio da altura
velocidade = 30

relogio = pygame.time.Clock()
rodando = True

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

    # C. Lógica de Fronteiras (O Quadrado não pode sair da tela)
    if pos_x < 0:
        pos_x = 0
    if pos_x > LARGURA - tamanho_quadrado:
        pos_x = LARGURA - tamanho_quadrado
    
    if pos_y < 0:
        pos_y = 0
    if pos_y > ALTURA - tamanho_quadrado:
        pos_y = ALTURA - tamanho_quadrado

    # D. Desenho (Renderização)
    tela.fill(PRETO) # Limpa a tela
    
    # Desenha o jogador (Surface, Cor, [x, y, largura, altura])
    pygame.draw.rect(tela, VERDE, (pos_x, pos_y, tamanho_quadrado, tamanho_quadrado))

    pygame.display.flip() # Atualiza a tela
    relogio.tick(60)      # Mantém a 60 FPS

pygame.quit()
