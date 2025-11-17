#!/usr/bin/env python3
"""🎮 게임 005 - PAC-MAN (팩맨)"""
import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRID = 20
FPS = 10
WHITE, BLACK, YELLOW, RED = (255,255,255), (0,0,0), (255,255,0), (255,0,0)

class PacMan:
    def __init__(self):
        self.x, self.y = 5, 5
        self.next_dir = (1, 0)
        self.dir = (1, 0)

    def move(self):
        nx, ny = self.x + self.next_dir[0], self.y + self.next_dir[1]
        if 0 <= nx < SCREEN_WIDTH // GRID and 0 <= ny < SCREEN_HEIGHT // GRID:
            self.x, self.y = nx, ny
            self.dir = self.next_dir

class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def move(self):
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.x = max(0, min(self.x, SCREEN_WIDTH // GRID - 1))
        self.y = max(0, min(self.y, SCREEN_HEIGHT // GRID - 1))

class PacManGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 PAC-MAN - 게임 005")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.pacman = PacMan()
        self.ghosts = [Ghost(9, 9), Ghost(8, 9)]
        self.pellets = {(x, y) for x in range(SCREEN_WIDTH // GRID)
                       for y in range(SCREEN_HEIGHT // GRID)}
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.pacman.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_dir = (0, 1)
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_dir = (1, 0)

    def update(self):
        if self.game_over:
            return

        self.pacman.move()

        if (self.pacman.x, self.pacman.y) in self.pellets:
            self.pellets.remove((self.pacman.x, self.pacman.y))
            self.score += 10

        for ghost in self.ghosts:
            ghost.move()
            if self.pacman.x == ghost.x and self.pacman.y == ghost.y:
                self.game_over = True

        if not self.pellets:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        for x, y in self.pellets:
            pygame.draw.circle(self.screen, WHITE, (x * GRID + GRID // 2, y * GRID + GRID // 2), 2)

        pygame.draw.circle(self.screen, YELLOW, (self.pacman.x * GRID + GRID // 2, self.pacman.y * GRID + GRID // 2), GRID // 2 - 2)

        for ghost in self.ghosts:
            pygame.draw.circle(self.screen, RED, (ghost.x * GRID + GRID // 2, ghost.y * GRID + GRID // 2), GRID // 2 - 2)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("GAME OVER" if not self.pellets else "YOU LOSE!", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    PacManGame().run()
