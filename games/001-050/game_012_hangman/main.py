#!/usr/bin/env python3
"""🎮 게임 012 - HANGMAN (행맨)"""
import pygame, random, sys
pygame.init()
SW, SH = 800, 600
FPS = 60
WHITE, BLACK, RED, GREEN = (255,255,255), (0,0,0), (255,0,0), (0,255,0)

class HangmanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 HANGMAN - 게임 012")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.words = ['PYTHON', 'PYGAME', 'COMPUTER', 'PROGRAMMING', 'HANGMAN', 'ALGORITHM']
        self.word = random.choice(self.words)
        self.guessed = set()
        self.wrong = 0
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.KEYDOWN:
                char = chr(event.key).upper() if 97 <= event.key <= 122 else None
                if char and char not in self.guessed:
                    self.guessed.add(char)
                    if char not in self.word:
                        self.wrong += 1

    def draw(self):
        self.screen.fill(BLACK)
        word_display = ''.join(c if c in self.guessed else '_' for c in self.word)
        word_text = self.font.render(word_display, True, GREEN)
        self.screen.blit(word_text, (50, 50))
        wrong_text = self.small_font.render(f"Wrong: {self.wrong}/6", True, RED if self.wrong > 3 else WHITE)
        self.screen.blit(wrong_text, (50, 150))
        guessed_text = self.small_font.render(f"Guessed: {' '.join(sorted(self.guessed))}", True, WHITE)
        self.screen.blit(guessed_text, (50, 200))

        if all(c in self.guessed for c in self.word):
            win_text = self.font.render("YOU WIN!", True, GREEN)
            self.screen.blit(win_text, (200, SH // 2))
        elif self.wrong >= 6:
            lose_text = self.font.render(f"GAME OVER! Word: {self.word}", True, RED)
            self.screen.blit(lose_text, (150, SH // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    HangmanGame().run()
