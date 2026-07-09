import pygame

# 1. Inicialização
pygame.init()

# 2. Criar a janela (largura, altura)
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Meu Primeiro Jogo")

# 3. Relógio para controlar o FPS
relogio = pygame.time.Clock()

rodando = True
while rodando:
    # --- Passo 1: Processar Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Se clicar no 'X' da janela
            rodando = False

    # --- Passo 2: Lógica do Jogo ---
    # (Ex: mover um personagem)

    # --- Passo 3: Renderização ---
    tela.fill((0, 0, 0))  # Limpa a tela com um cinza escuro
    
    # Desenha um círculo azul no centro
    pygame.draw.circle(tela, (0, 0, 255), (400, 300), 50)

    pygame.display.flip()  # Atualiza o conteúdo da tela
    relogio.tick(60)       # Garante que o jogo rode a 60 FPS

pygame.quit()
