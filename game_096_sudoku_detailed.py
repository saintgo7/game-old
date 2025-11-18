#!/usr/bin/env python3
"""🧩 Sudoku (게임 096) - 숫자 로직 퍼즐"""
import pygame, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from puzzle_game_template import PuzzleGame
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class SudokuGame(PuzzleGame):
    """Sudoku 게임"""
    def __init__(self):
        super().__init__("Sudoku")
        self.grid = [[0]*9 for _ in range(9)]
        self.solution = [[i for i in range(1, 10)] for _ in range(9)]
        self.selected = None
        self.generate_puzzle()

    def generate_puzzle(self):
        """퍼즐 생성"""
        for i in range(9):
            for j in range(9):
                if random.random() < 0.6:
                    self.grid[i][j] = random.randint(1, 9)

    def handle_input(self, keys):
        """입력 처리"""
        if pygame.key.get_pressed()[pygame.K_1]:
            self._number_pressed(1)
        elif pygame.key.get_pressed()[pygame.K_2]:
            self._number_pressed(2)
        elif pygame.key.get_pressed()[pygame.K_3]:
            self._number_pressed(3)

    def _number_pressed(self, num):
        """숫자 입력"""
        pass

    def _check_win(self):
        """승리 조건"""
        return all(all(cell != 0 for cell in row) for row in self.grid)

    def draw(self):
        """그리기"""
        self.screen.fill(self.theme.bg_color)
        
        # 그리드
        cell_size = 50
        for i in range(9):
            for j in range(9):
                x, y = 50 + j * cell_size, 50 + i * cell_size
                pygame.draw.rect(self.screen, (100, 100, 100), (x, y, cell_size, cell_size), 1)
                if self.grid[i][j] != 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(self.grid[i][j]), True, Color.WHITE)
                    self.screen.blit(text, (x + 15, y + 15))
        
        # UI
        score = self.font.render(f"Score: {self.score}", True, Color.GREEN)
        self.screen.blit(score, (10, 520))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()
