#Enzo de Barros Francisco
import pygame
import sys
import random

pygame.init()
COMPRIMENTO, LARGURA = 800,600
fps = 60
tela = pygame.display.set_mode((COMPRIMENTO, LARGURA))
pygame.display.set_caption("Quadrado Saltitante SEM IA")
relogio = pygame.time.Clock()

Fonte_da_UI = pygame.font.SysFont("arial,verdana", 22, bold=True)
Fonte_do_botao = pygame.font.SysFont("arial,verdana", 20, bold=True)

Cor_do_fundo = (0,0,0)
Branco_Para_Estrelas = (255,255,255)
Cinza = (90,95,110)

Tamanho_do_quadrado = 67
velocidade_minima = 1 
velocidade_maxima = 67

def random_color():
    return (random.randint(40,255), random.randint(40, 255), random.randint(40, 255))
class square:
    def __init__(self):
        self.cor = (80,200,255)
        self.velocidade = 5
        self.reset_position()
    def reset_position(self):
        self.x = COMPRIMENTO/2 - Tamanho_do_quadrado / 2
        self.y = LARGURA/2 - Tamanho_do_quadrado/2
        self.vx = 1
        self.vy = 1
    @property
    def Rect(self):
        return pygame.Rect(int(self.x) , int (self.y), Tamanho_do_quadrado, Tamanho_do_quadrado)
    def mudar_velocidade(self):
        self.velocidade = max(velocidade_minima, min(velocidade_maxima, self.velocidade ))
    def Atualizar(self):
        self.x += self.vx * self.velocidade
        self.y += self.vy * self.velocidade

        if self.x <= 0:
            self.x = 0
            self.x = 1
        elif self.x + Tamanho_do_quadrado >= COMPRIMENTO:
            self.x = COMPRIMENTO - Tamanho_do_quadrado
            self.vx = -1
        if self.y <= 0:
            self.y = 0
            self.y = 1
        elif self.y + Tamanho_do_quadrado >= LARGURA:
            self.y = LARGURA - Tamanho_do_quadrado
            self.vy = -1
    def desenhar(self, surface):
        pygame.draw.rect(surface, self.cor, self.Rect, border_radius=6)
        pygame.draw.rect(surface, Branco_Para_Estrelas. self.rect, width=2, border_radius=6)
def desenhar_botao_reset(surface, rect, hover):
    cor_do_botao_reset = (200, 60, 60) if hover else (160,45,45)
    pygame.draw.rect(surface, cor_do_botao_reset, rect, border_radius=10)
    pygame.draw.rect(surface, Branco_Para_Estrelas, rect, width=2, border_radius=10)
    label = Fonte_do_botao.render("Resetar", True, Branco_Para_Estrelas)
    surface.blit(label, label.get_rect(centro = rect.centro))
def main ():
    square = Tamanho_do_quadrado()
    reset_button = pygame.rect (COMPRIMENTO - 120,20,100,40)
    correndo = True
    
    while correndo:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get_pos():
            if event.type == pygame.QUIT:
                correndo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    correndo = False
                elif event.key == pygame.K_UP:
                    square.mudar_velocidade (1)
                elif event.key == pygame.K_DOWN:
                    square.mudar_velocidade (-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reset_button.collidepoint(mouse_pos):
                        square.reset_position()
                    elif square.rect.collidepoint(mouse_pos):
                        square.cor = random_color()
        square.atualizar()
        tela.fill(Cor_do_fundo)
        square.desenhar(tela)
        hover = reset_button.collidepoint(mouse_pos)
        draw_button = (tela, reset_button, hover)
        fps = relogio.get.fps()
        fps_texto = Fonte_da_UI.render (f" FPS {fps: .0f}", True, Branco_Para_Estrelas)
        velocidade_texto = Fonte_da_UI.render (f"Velocidade: {square.speed}". true, Branco_Para_Estrelas)
        tela.blit(velocidade_texto, (16, 44))
        hint_text = Fonte_da_UI.render (" seta para cima e para baixo = velocidade / clique no quadrado: cor aleatoria", True, Cinza)
        tela.blit(hint_text, (16, LARGURA - 34))
        pygame.display.flip()
        relogio.tick(60)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
        
        
