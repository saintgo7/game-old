#!/usr/bin/env python3
"""🎮 게임 013 - SIMON SAYS (사이먼 세이즈)"""
import pygame, random, sys
pygame.init()
SW, SH = 500, 500
WHITE, BLACK, RED, BLUE, GREEN, YELLOW = (255,255,255), (0,0,0), (255,0,0), (0,0,255), (0,255,0), (255,255,0)

class SimonGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 SIMON - 게임 013")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.colors = [RED, BLUE, GREEN, YELLOW]
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.running = True
        self.add_to_sequence()

    def add_to_sequence(self):
        self.sequence.append(random.randint(0, 3))
        self.player_sequence = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                color_idx = (0 if x < SW // 2 else 1) + (0 if y < SH // 2 else 2)
                if color_idx < 4:
                    self.player_sequence.append(color_idx)
                    if len(self.player_sequence) <= len(self.sequence):
                        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
                            self.level = 1
                            self.sequence = []
                            self.add_to_sequence()
                        elif len(self.player_sequence) == len(self.sequence):
                            self.level += 1
                            self.add_to_sequence()

    def draw(self):
        self.screen.fill(BLACK)
        grid_w, grid_h = SW // 2, SH // 2
        for i, color in enumerate(self.colors):
            x = (i % 2) * grid_w
            y = (i // 2) * grid_h
            pygame.draw.rect(self.screen, color, (x, y, grid_w, grid_h))
            pygame.draw.rect(self.screen, WHITE, (x, y, grid_w, grid_h), 2)

        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (SW // 2 - 80, SH // 2 - 20))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    SimonGame().run()
