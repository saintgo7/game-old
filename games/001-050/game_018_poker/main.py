#!/usr/bin/env python3
"""🎮 게임 018 - POKER (포커)"""
import pygame, random, sys
pygame.init()
SW, SH = 800, 600
WHITE, BLACK = (255,255,255), (0,0,0)

class PokerGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 POKER - 게임 018")
        self.font = pygame.font.Font(None, 32)
        self.deck = [(i, j) for i in range(1, 14) for j in range(4)]
        random.shuffle(self.deck)
        self.player_hand = self.deck[:5]
        self.ai_hand = self.deck[5:10]
        self.player_score = random.randint(1, 10)
        self.ai_score = random.randint(1, 10)
        self.running = True

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        txt1 = self.font.render(f"Your Hand: {len(self.player_hand)} cards | Score: {self.player_score}", True, WHITE)
        txt2 = self.font.render(f"AI Hand: {len(self.ai_hand)} cards | Score: {self.ai_score}", True, WHITE)

        if self.player_score > self.ai_score:
            txt3 = self.font.render("YOU WIN!", True, (0,255,0))
        elif self.ai_score > self.player_score:
            txt3 = self.font.render("AI WINS!", True, (255,0,0))
        else:
            txt3 = self.font.render("TIE!", True, (255,255,0))

        self.screen.blit(txt1, (50, 100))
        self.screen.blit(txt2, (50, 200))
        self.screen.blit(txt3, (350, 300))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    PokerGame().run()
