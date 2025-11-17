#!/usr/bin/env python3
"""게임 022 - CENTIPEDE"""
import pygame, random, sys
pygame.init()
S = 800
WHITE, BLACK = (255,255,255), (0,0,0)
class Game:
    def __init__(self):
        self.s = pygame.display.set_mode((S, S))
        pygame.display.set_caption("게임 022 - CENTIPEDE")
        self.p = pygame.Rect(S//2, S-50, 40, 40)
        self.e = [pygame.Rect(i*30, j*30, 20, 20) for i in range(5) for j in range(5)]
        self.b = []
        self.run = True
    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE): self.run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and self.p.x > 0: self.p.x -= 20
                if e.key == pygame.K_RIGHT and self.p.x < S-40: self.p.x += 20
                if e.key == pygame.K_SPACE: self.b.append(pygame.Rect(self.p.x+20, self.p.y, 5, 20))
    def update(self):
        for b in self.b[:]:
            b.y -= 10
            if b.y < 0: self.b.remove(b)
        for en in self.e[:]:
            en.x += random.choice([-1, 1])
            for b in self.b[:]:
                if b.colliderect(en):
                    self.e.remove(en)
                    self.b.remove(b)
                    break
    def draw(self):
        self.s.fill(BLACK)
        pygame.draw.rect(self.s, (0,255,0), self.p)
        for en in self.e: pygame.draw.rect(self.s, (255,0,0), en)
        for b in self.b: pygame.draw.rect(self.s, WHITE, b)
        pygame.display.flip()
    def main(self):
        c = pygame.time.Clock()
        while self.run:
            self.handle()
            self.update()
            self.draw()
            c.tick(60)
        pygame.quit()
if __name__ == "__main__": Game().main()
