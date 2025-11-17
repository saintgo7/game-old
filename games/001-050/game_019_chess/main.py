#!/usr/bin/env python3
"""🎮 게임 019 - CHESS (체스 - 간단 버전)"""
import pygame, sys
pygame.init()
SW = 800
GS = 8
CS = SW // GS
WHITE, BLACK, GRAY = (255,255,255), (0,0,0), (128,128,128)

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SW, SW))
        pygame.display.set_caption("🎮 CHESS - 게임 019")
        self.board = [[None]*GS for _ in range(GS)]
        for i in range(GS):
            self.board[1][i] = ('p', 'white')
            self.board[6][i] = ('p', 'black')
        for p, row in [('r', 0), ('r', 7), ('n', 0), ('n', 7), ('b', 0), ('b', 7), ('q', 0), ('q', 7), ('k', 0), ('k', 7)]:
            cols = [0, 7] if p == 'r' else [1, 6] if p == 'n' else [2, 5] if p == 'b' else [3] if p == 'q' else [4]
            for col in cols:
                self.board[row][col] = (p, 'white' if row == 0 else 'black')
        self.selected = None
        self.running = True

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                self.running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos[0] // CS, e.pos[1] // CS
                if self.selected is None:
                    if self.board[y][x]:
                        self.selected = (y, x)
                else:
                    if (y, x) != self.selected:
                        self.board[y][x] = self.board[self.selected[0]][self.selected[1]]
                        self.board[self.selected[0]][self.selected[1]] = None
                    self.selected = None

    def draw(self):
        for i in range(GS):
            for j in range(GS):
                color = WHITE if (i+j)%2==0 else GRAY
                pygame.draw.rect(self.screen, color, (j*CS, i*CS, CS, CS))
                if self.selected == (i, j):
                    pygame.draw.rect(self.screen, (255,0,0), (j*CS, i*CS, CS, CS), 3)
                if self.board[i][j]:
                    p, c = self.board[i][j]
                    txt_color = WHITE if c == 'white' else BLACK
                    font = pygame.font.Font(None, 48)
                    t = font.render(p.upper(), True, txt_color)
                    self.screen.blit(t, (j*CS+10, i*CS+10))
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    ChessGame().run()
