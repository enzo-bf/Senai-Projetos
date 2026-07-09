#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QUADRADO QUICANTE
Um quadrado se move pela tela e rebate nas bordas.

Controles:
  - Seta CIMA   : aumenta a velocidade
  - Seta BAIXO  : diminui a velocidade
  - Clique dentro do quadrado : muda para uma cor aleatória
  - Botão "RESET" (canto superior direito) : volta o quadrado para o centro
  - ESC : sai

Requisitos: pip install pygame
"""

import sys
import random

import pygame

# --------------------------------------------------------------------------- #
# CONFIGURAÇÃO
# --------------------------------------------------------------------------- #

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quadrado Quicante")
clock = pygame.time.Clock()

FONT_UI = pygame.font.SysFont("arial,verdana", 22, bold=True)
FONT_BTN = pygame.font.SysFont("arial,verdana", 20, bold=True)

BG_COLOR = (25, 28, 38)
WHITE = (255, 255, 255)
GRAY = (90, 95, 110)

SQUARE_SIZE = 60
MIN_SPEED = 1
MAX_SPEED = 20

# --------------------------------------------------------------------------- #
# ESTADO DO QUADRADO
# --------------------------------------------------------------------------- #

def random_color():
    return (random.randint(40, 255), random.randint(40, 255), random.randint(40, 255))


class Square:
    def __init__(self):
        self.color = (80, 200, 255)
        self.speed = 5
        self.reset_position()

    def reset_position(self):
        self.x = WIDTH / 2 - SQUARE_SIZE / 2
        self.y = HEIGHT / 2 - SQUARE_SIZE / 2
        self.vx = 1  # direção horizontal (1 ou -1)
        self.vy = 1  # direção vertical (1 ou -1)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), SQUARE_SIZE, SQUARE_SIZE)

    def change_speed(self, delta):
        self.speed = max(MIN_SPEED, min(MAX_SPEED, self.speed + delta))

    def update(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        # rebate nas bordas horizontais
        if self.x <= 0:
            self.x = 0
            self.vx = 1
        elif self.x + SQUARE_SIZE >= WIDTH:
            self.x = WIDTH - SQUARE_SIZE
            self.vx = -1

        # rebate nas bordas verticais
        if self.y <= 0:
            self.y = 0
            self.vy = 1
        elif self.y + SQUARE_SIZE >= HEIGHT:
            self.y = HEIGHT - SQUARE_SIZE
            self.vy = -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=6)


# --------------------------------------------------------------------------- #
# BOTÃO RESET
# --------------------------------------------------------------------------- #

def draw_button(surface, rect, hover):
    color = (200, 60, 60) if hover else (160, 45, 45)
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, WHITE, rect, width=2, border_radius=10)
    label = FONT_BTN.render("RESET", True, WHITE)
    surface.blit(label, label.get_rect(center=rect.center))


# --------------------------------------------------------------------------- #
# LOOP PRINCIPAL
# --------------------------------------------------------------------------- #

def main():
    square = Square()
    reset_button = pygame.Rect(WIDTH - 120, 20, 100, 40)
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    square.change_speed(1)
                elif event.key == pygame.K_DOWN:
                    square.change_speed(-1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reset_button.collidepoint(mouse_pos):
                        square.reset_position()
                    elif square.rect.collidepoint(mouse_pos):
                        square.color = random_color()

        square.update()

        # -------- desenho --------
        screen.fill(BG_COLOR)
        square.draw(screen)

        hover = reset_button.collidepoint(mouse_pos)
        draw_button(screen, reset_button, hover)

        fps = clock.get_fps()
        fps_text = FONT_UI.render(f"FPS: {fps:.0f}", True, WHITE)
        speed_text = FONT_UI.render(f"Velocidade: {square.speed}", True, WHITE)
        screen.blit(fps_text, (16, 16))
        screen.blit(speed_text, (16, 44))

        hint_text = FONT_UI.render("↑ / ↓ velocidade   |   clique no quadrado: cor aleatória", True, GRAY)
        screen.blit(hint_text, (16, HEIGHT - 34))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()