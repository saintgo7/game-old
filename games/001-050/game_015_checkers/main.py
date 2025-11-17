#!/usr/bin/env python3
"""🎮 게임 015 - CHECKERS (체커스)"""
import pygame, sys
pygame.init()
SW = 800
GRID = 8
CS = SW // GRID
BG = (200, 100, 50)
BLACK, WHITE, RED, YELLOW = (0,0,0), (255,255,255), (255,0,0), (255,255,0)

class CheckersGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SW))
        pygame.display.set_caption("🎮 CHECKERS - 게임 015")
        self.board = [[None] * GRID for _ in range(GRID)]
        for i in range(GRID):
            for j in range(GRID):
                if (i + j) % 2 == 1:
                    if i < 3: self.board[i][j] = ('red', False)
                    elif i > 4: self.board[i][j] = ('white', False)
        self.selected = None
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // CS, event.pos[1] // CS
                if self.board[y][x] and self.board[y][x][0] == 'red':
                    self.selected = (y, x) if self.selected != (y, x) else None

    def draw(self):
        for i in range(GRID):
            for j in range(GRID):
                color = WHITE if (i + j) % 2 == 0 else (220, 180, 140)
                pygame.draw.rect(self.screen, color, (j * CS, i * CS, CS, CS))
                if self.selected == (i, j):
                    pygame.draw.rect(self.screen, YELLOW, (j * CS, i * CS, CS, CS), 5)
                if self.board[i][j]:
                    pc = RED if self.board[i][j][0] == 'red' else (100, 100, 100)
                    pygame.draw.circle(self.screen, pc, (j * CS + CS // 2, i * CS + CS // 2), CS // 3)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    CheckersGame().run()
