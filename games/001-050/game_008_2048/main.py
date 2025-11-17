#!/usr/bin/env python3
"""🎮 게임 008 - 2048 (2048 퍼즐)"""
import pygame
import random
import sys

pygame.init()

GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
SCREEN_SIZE = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * MARGIN
FPS = 60
WHITE, BLACK, GRAY = (255,255,255), (0,0,0), (128,128,128)

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 50))
        pygame.display.set_caption("🎮 2048 - 게임 008")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()
        self.score = 0
        self.running = True
        self.game_over = False

    def add_new_tile(self):
        while True:
            r, c = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if self.grid[r][c] == 0:
                self.grid[r][c] = random.choice([2, 2, 2, 4])
                break

    def move(self, direction):
        moved = False
        for _ in range(GRID_SIZE):
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if direction == 'L':
                        if j > 0 and self.grid[i][j] != 0 and self.grid[i][j-1] == 0:
                            self.grid[i][j-1] = self.grid[i][j]
                            self.grid[i][j] = 0
                            moved = True
                        elif j > 0 and self.grid[i][j] != 0 and self.grid[i][j-1] == self.grid[i][j]:
                            self.grid[i][j-1] *= 2
                            self.score += self.grid[i][j-1]
                            self.grid[i][j] = 0
                            moved = True
        return moved

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.move('L'):
                            self.add_new_tile()
                    elif event.key == pygame.K_RIGHT:
                        self.grid = [row[::-1] for row in self.grid]
                        if self.move('L'):
                            self.grid = [row[::-1] for row in self.grid]
                            self.add_new_tile()
                        else:
                            self.grid = [row[::-1] for row in self.grid]
                    elif event.key == pygame.K_UP:
                        self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
                        if self.move('L'):
                            self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
                            self.add_new_tile()
                        else:
                            self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
                    elif event.key == pygame.K_DOWN:
                        self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
                        self.grid = [row[::-1] for row in self.grid]
                        if self.move('L'):
                            self.grid = [row[::-1] for row in self.grid]
                            self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
                            self.add_new_tile()
                        else:
                            self.grid = [row[::-1] for row in self.grid]
                            self.grid = [[self.grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

                    if any(2048 in row for row in self.grid):
                        self.game_over = True

    def draw(self):
        self.screen.fill(WHITE)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = j * (CELL_SIZE + MARGIN) + MARGIN
                y = i * (CELL_SIZE + MARGIN) + MARGIN
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                if self.grid[i][j] > 0:
                    text = self.font.render(str(self.grid[i][j]), True, BLACK)
                    self.screen.blit(text, (x + CELL_SIZE // 2 - 20, y + CELL_SIZE // 2 - 20))

        score_text = self.small_font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, SCREEN_SIZE + 10))

        if self.game_over:
            text = self.small_font.render("YOU WIN!", True, BLACK)
            self.screen.blit(text, (SCREEN_SIZE // 2 - 50, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    Game2048().run()
