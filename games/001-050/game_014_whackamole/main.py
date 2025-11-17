#!/usr/bin/env python3
"""🎮 게임 014 - WHACK-A-MOLE (두더지 잡기)"""
import pygame, random, sys
pygame.init()
SW, SH = 600, 600
WHITE, BLACK, BROWN, GRAY = (255,255,255), (0,0,0), (139,69,19), (128,128,128)

class WhackGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 WHACK-A-MOLE - 게임 014")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.grid = 3
        self.cell_size = SW // self.grid
        self.mole_pos = None
        self.score = 0
        self.time = 30
        self.last_time = pygame.time.get_ticks()
        self.running = True
        self.spawn_mole()

    def spawn_mole(self):
        self.mole_pos = (random.randint(0, self.grid - 1), random.randint(0, self.grid - 1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.time > 0:
                x, y = event.pos
                col, row = x // self.cell_size, y // self.cell_size
                if (row, col) == self.mole_pos:
                    self.score += 1
                    self.spawn_mole()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:
            self.time -= 1
            self.last_time = current_time

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(self.grid + 1):
            pygame.draw.line(self.screen, GRAY, (i * self.cell_size, 0), (i * self.cell_size, SW))
            pygame.draw.line(self.screen, GRAY, (0, i * self.cell_size), (SW, i * self.cell_size))

        if self.mole_pos:
            r, c = self.mole_pos
            x = c * self.cell_size + self.cell_size // 2
            y = r * self.cell_size + self.cell_size // 2
            pygame.draw.circle(self.screen, BROWN, (x, y), self.cell_size // 3)

        score_text = self.font.render(f"Score: {self.score} Time: {self.time}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.time <= 0:
            game_over_text = self.font.render(f"GAME OVER! Final: {self.score}", True, WHITE)
            self.screen.blit(game_over_text, (SW // 2 - 150, SH // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    WhackGame().run()
