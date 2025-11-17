#!/usr/bin/env python3
"""🎮 게임 011 - MEMORY GAME (메모리 게임)"""
import pygame, random, sys

pygame.init()
SCREEN_SIZE = 600
GRID = 4
CELL_SIZE = SCREEN_SIZE // GRID
FPS = 60
WHITE, BLACK, GRAY, GREEN, RED = (255,255,255), (0,0,0), (128,128,128), (0,255,0), (255,0,0)

class MemoryGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 50))
        pygame.display.set_caption("🎮 MEMORY - 게임 011")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        nums = list(range(1, GRID * GRID // 2 + 1)) * 2
        random.shuffle(nums)
        self.board = [[nums[i * GRID + j] for j in range(GRID)] for i in range(GRID)]
        self.revealed = [[False] * GRID for _ in range(GRID)]
        self.first_click = None
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if not self.revealed[y][x]:
                    if self.first_click is None:
                        self.first_click = (y, x)
                        self.revealed[y][x] = True
                    else:
                        fy, fx = self.first_click
                        if self.board[y][x] == self.board[fy][fx]:
                            self.revealed[y][x] = True
                            self.score += 1
                            self.first_click = None
                        else:
                            pygame.time.wait(500)
                            self.revealed[y][x] = True
                            pygame.time.wait(500)
                            self.revealed[y][x] = False
                            self.revealed[fy][fx] = False
                            self.first_click = None

                    if all(all(row) for row in self.revealed):
                        self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(GRID):
            for j in range(GRID):
                x, y = j * CELL_SIZE, i * CELL_SIZE
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 2)
                if self.revealed[i][j]:
                    text = self.font.render(str(self.board[i][j]), True, GREEN)
                    self.screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 3))

        score_text = self.font.render(f"Matched: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_SIZE + 10))
        if self.game_over:
            text = self.font.render("YOU WIN!", True, WHITE)
            self.screen.blit(text, (SCREEN_SIZE // 2 - 60, SCREEN_SIZE // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    MemoryGame().run()
