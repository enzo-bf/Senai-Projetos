import pygame
import random

# 1. Inicialização
pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Exercício 2: Seguidor de Mouse")

# Cores iniciais
PRETO = (0, 0, 0)
cor_circulo = [255, 0, 0] # Vermelho (usamos lista para poder mudar os valores)

relogio = pygame.time.Clock()
rodando = True

# --- LOOP PRINCIPAL ---
while rodando:
    # A. Tratamento de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Detecta o clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Muda para uma cor aleatória ao clicar
            cor_circulo = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    # B. Lógica: Obter a posição atual do mouse
    posicao_mouse = pygame.mouse.get_pos() # Retorna uma tupla (x, y)

    # C. Renderização
    #tela.fill(PRETO)
    
    # Desenha o círculo na posição do mouse
    # pygame.draw.circle(superficie, cor, centro(x,y), raio)
    pygame.draw.circle(tela, cor_circulo, posicao_mouse, 30)

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()