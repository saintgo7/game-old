#!/usr/bin/env python3
"""🎮 게임 016 - CONNECT FOUR (4목 게임)"""
import pygame, sys
pygame.init()
SW, SH = 700, 600
BS = 100
BG, BLACK, WHITE, RED, YELLOW = (0,0,100), (0,0,0), (255,255,255), (255,0,0), (255,255,0)

class C4Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption("🎮 CONNECT4 - 게임 016")
        self.board = [[0] * 7 for _ in range(6)]
        self.turn = 1
        self.running = True

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and self.turn != 0:
                col = e.pos[0] // BS
                if col < 7 and any(self.board[r][col] == 0 for r in range(6)):
                    for r in range(5, -1, -1):
                        if self.board[r][col] == 0:
                            self.board[r][col] = self.turn
                            if self.check_win(r, col):
                                self.turn = 0
                            else:
                                self.turn = 3 - self.turn
                            break

    def check_win(self, r, c):
        dirs = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in dirs:
            cnt = 1
            for i in range(1, 4):
                nr, nc = r + i*dr, c + i*dc
                if 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == self.board[r][c]:
                    cnt += 1
            for i in range(1, 4):
                nr, nc = r - i*dr, c - i*dc
                if 0 <= nr < 6 and 0 <= nc < 7 and self.board[nr][nc] == self.board[r][c]:
                    cnt += 1
            if cnt >= 4: return True
        return False

    def draw(self):
        self.screen.fill(BG)
        for r in range(6):
            for c in range(7):
                col = BLACK
                if self.board[r][c] == 1: col = RED
                elif self.board[r][c] == 2: col = YELLOW
                pygame.draw.circle(self.screen, col, (c*BS+BS//2, r*BS+BS//2), BS//2 - 5)
        if self.turn == 0:
            font = pygame.font.Font(None, 48)
            txt = font.render("GAME OVER", True, WHITE)
            self.screen.blit(txt, (200, 550))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    C4Game().run()
