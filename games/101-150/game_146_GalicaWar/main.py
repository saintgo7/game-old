#!/usr/bin/env python3
"""🎮 게임 146 - GALICAWAR"""
import pygame, random, sys
pygame.init()
S = 800
WHITE, BLACK = (255,255,255), (0,0,0)

class Game:
    def __init__(self):
        self.s = pygame.display.set_mode((S, S))
        pygame.display.set_caption("🎮 게임 146")
        self.p = pygame.Rect(S//2, S-50, 40, 40)
        self.run = True

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self.run = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.run = False

    def draw(self):
        self.s.fill(BLACK)
        pygame.draw.rect(self.s, (0,255,0), self.p)
        font = pygame.font.Font(None, 48)
        txt = font.render("게임 146", True, WHITE)
        self.s.blit(txt, (S//3, S//2))
        pygame.display.flip()

    def main(self):
        c = pygame.time.Clock()
        while self.run:
            self.handle()
            self.draw()
            c.tick(60)
        pygame.quit()

if __name__ == "__main__":
    Game().main()
