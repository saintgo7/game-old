#!/usr/bin/env python3
"""🎮 게임 020 - DONKEY KONG (동키콩)"""
import pygame, random, sys
pygame.init()
SW, SH = 800, 600
WHITE, BLACK, BROWN, RED = (255,255,255), (0,0,0), (139,69,19), (255,0,0)

class DonkeyKongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 DONKEY KONG - 게임 020")
        self.player = pygame.Rect(50, 500, 40, 40)
        self.kong = pygame.Rect(700, 50, 50, 50)
        self.barrels = []
        self.goal = pygame.Rect(700, 500, 50, 50)
        self.score = 0
        self.running = True
        self.barrel_timer = 0

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and self.player.left > 0:
                    self.player.x -= 20
                elif e.key == pygame.K_RIGHT and self.player.right < SW:
                    self.player.x += 20
                elif e.key == pygame.K_UP and self.player.top > 0:
                    self.player.y -= 20

    def update(self):
        self.barrel_timer += 1
        if self.barrel_timer > 30:
            self.barrels.append(pygame.Rect(self.kong.x, self.kong.y, 20, 20))
            self.barrel_timer = 0

        for barrel in self.barrels[:]:
            barrel.x += random.choice([-2, 2])
            barrel.y += 3
            if barrel.top > SH:
                self.barrels.remove(barrel)
                self.score += 1
            elif barrel.colliderect(self.player):
                self.running = False

        if self.player.colliderect(self.goal):
            self.score += 100
            self.player.x, self.player.y = 50, 500

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, RED, self.player)
        pygame.draw.rect(self.screen, BROWN, self.kong)
        pygame.draw.rect(self.screen, (255,215,0), self.goal)
        for barrel in self.barrels:
            pygame.draw.circle(self.screen, (200,100,0), barrel.center, 10)

        font = pygame.font.Font(None, 36)
        txt = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(txt, (10, 10))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    DonkeyKongGame().run()
