#!/usr/bin/env python3
"""🎮 게임 010 - TIC-TAC-TOE (틱택토)"""
import pygame
import sys

pygame.init()

SCREEN_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = SCREEN_SIZE // GRID_SIZE
FPS = 60
WHITE, BLACK, GRAY = (255,255,255), (0,0,0), (128,128,128)
BLUE, RED = (0,0,255), (255,0,0)

class TicTacToeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 50))
        pygame.display.set_caption("🎮 TIC-TAC-TOE - 게임 010")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)

        self.board = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player = 'X'
        self.ai = 'O'
        self.running = True
        self.game_over = False
        self.winner = None

    def minimax(self, depth, is_max):
        score = self.evaluate()
        if score == 10: return score - depth
        if score == -10: return score + depth
        if self.is_full(): return 0

        if is_max:
            best = -1000
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.board[i][j] == '.':
                        self.board[i][j] = self.ai
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[i][j] = '.'
            return best
        else:
            best = 1000
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.board[i][j] == '.':
                        self.board[i][j] = self.player
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[i][j] = '.'
            return best

    def ai_move(self):
        best_val = -1000
        best_move = None
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == '.':
                    self.board[i][j] = self.ai
                    val = self.minimax(0, False)
                    self.board[i][j] = '.'
                    if val > best_val:
                        best_val = val
                        best_move = (i, j)
        if best_move:
            self.board[best_move[0]][best_move[1]] = self.ai

    def evaluate(self):
        lines = [[(i, j) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
        lines += [[(i, j) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
        lines += [[(i, i) for i in range(GRID_SIZE)]]
        lines += [[(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)]]

        for line in lines:
            if all(self.board[i][j] == self.ai for i, j in line):
                return 10
            if all(self.board[i][j] == self.player for i, j in line):
                return -10
        return 0

    def is_full(self):
        return all(self.board[i][j] != '.' for i in range(GRID_SIZE) for j in range(GRID_SIZE))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                x, y = event.pos
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if self.board[row][col] == '.':
                    self.board[row][col] = self.player
                    self.winner = self.evaluate()
                    if not self.winner and not self.is_full():
                        self.ai_move()
                        self.winner = self.evaluate()
                    if self.winner or self.is_full():
                        self.game_over = True

    def draw(self):
        self.screen.fill(WHITE)

        for i in range(GRID_SIZE + 1):
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), 2)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), 2)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                text = self.font.render(self.board[i][j], True, BLUE if self.board[i][j] == 'X' else RED)
                self.screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 4))

        if self.game_over:
            if self.winner == 10:
                msg = "AI WINS!"
            elif self.winner == -10:
                msg = "YOU WIN!"
            else:
                msg = "DRAW!"
            text = self.small_font.render(msg, True, BLACK)
            self.screen.blit(text, (SCREEN_SIZE // 2 - 80, SCREEN_SIZE + 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    TicTacToeGame().run()
