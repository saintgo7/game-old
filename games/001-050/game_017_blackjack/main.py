#!/usr/bin/env python3
"""🎮 게임 017 - BLACKJACK (블랙잭)"""
import pygame, random, sys
pygame.init()
SW, SH = 800, 600
WHITE, BLACK, GREEN, RED = (255,255,255), (0,0,0), (0,200,0), (255,0,0)

class BlackjackGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 BLACKJACK - 게임 017")
        self.font = pygame.font.Font(None, 48)
        self.deck = [2]*4 + [3]*4 + [4]*4 + [5]*4 + [6]*4 + [7]*4 + [8]*4 + [9]*4 + [10]*4 + [10]*4 + [10]*4 + [11]*4
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop()]
        self.running, self.game_over = True, False

    def get_score(self, hand):
        score = sum(hand)
        aces = hand.count(11)
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False
            elif e.type == pygame.KEYDOWN and not self.game_over:
                if e.key == pygame.K_h and self.get_score(self.player_hand) < 21:
                    self.player_hand.append(self.deck.pop())
                elif e.key == pygame.K_s:
                    self.dealer_hand.append(self.deck.pop())
                    while self.get_score(self.dealer_hand) < 17:
                        self.dealer_hand.append(self.deck.pop())
                    self.game_over = True

    def draw(self):
        self.screen.fill(GREEN)
        py, dy = self.get_score(self.player_hand), self.get_score(self.dealer_hand)
        p_txt = self.font.render(f"Player: {py}", True, WHITE)
        d_txt = self.font.render(f"Dealer: {dy}", True, WHITE)
        self.screen.blit(p_txt, (50, 100))
        self.screen.blit(d_txt, (50, 200))

        if self.game_over:
            if py > 21: result = "You Bust!"
            elif dy > 21 or py > dy: result = "You Win!"
            elif py < dy: result = "Dealer Wins!"
            else: result = "Tie!"
            r_txt = self.font.render(result, True, WHITE)
            self.screen.blit(r_txt, (200, SH // 2))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    BlackjackGame().run()
