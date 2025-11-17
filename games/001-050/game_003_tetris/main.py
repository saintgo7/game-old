#!/usr/bin/env python3
"""
🎮 게임 003 - TETRIS (테트리스)
떨어지는 테트로미노 블록을 회전하고 이동시켜 가로줄을 완성시키는 퍼즐 게임입니다.
"""

import pygame
import random
import sys

pygame.init()

# 설정
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
FPS = 60

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Cyan
    (255, 165, 0),    # Orange
]

# 테트로미노 블록 정의
TETROMINOS = [
    [[1, 1], [1, 1]],                    # O
    [[0, 1, 0], [1, 1, 1]],             # T
    [[1, 0], [1, 0], [1, 1]],           # L
    [[0, 1], [0, 1], [1, 1]],           # J
    [[1, 1, 0], [0, 1, 1]],             # S
    [[0, 1, 1], [1, 1, 0]],             # Z
    [[1], [1], [1], [1]],               # I
]


class Tetromino:
    """테트로미노 블록"""
    def __init__(self):
        self.shape = random.choice(TETROMINOS)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """블록 회전"""
        original = self.shape
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))]
                      for x in range(len(self.shape[0]) - 1, -1, -1)]
        return self.shape

    def move(self, dx, dy):
        """블록 이동"""
        self.x += dx
        self.y += dy

    def get_cells(self):
        """블록이 차지하는 셀 반환"""
        cells = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    cells.append((self.x + x, self.y + y))
        return cells


class Grid:
    """게임 그리드"""
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def is_valid(self, tetromino):
        """테트로미노가 유효한 위치에 있는지 확인"""
        for x, y in tetromino.get_cells():
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x]:
                return False
        return True

    def place(self, tetromino):
        """테트로미노를 그리드에 배치"""
        for x, y in tetromino.get_cells():
            if 0 <= y < GRID_HEIGHT:
                self.grid[y][x] = tetromino.color

    def clear_lines(self):
        """완성된 줄 제거"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                self.grid.pop(y)
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared

    def draw(self, screen):
        """그리드 그리기"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], rect)
                pygame.draw.rect(screen, GRAY, rect, 1)


class TetrisGame:
    """테트리스 게임"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 50))
        pygame.display.set_caption("🎮 TETRIS - 게임 003")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.grid = Grid()
        self.current = Tetromino()
        self.score = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 30

        self.running = True
        self.game_over = False

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif not self.game_over:
                    if event.key == pygame.K_LEFT:
                        self.current.move(-1, 0)
                        if not self.grid.is_valid(self.current):
                            self.current.move(1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.current.move(1, 0)
                        if not self.grid.is_valid(self.current):
                            self.current.move(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.current.move(0, 1)
                        if not self.grid.is_valid(self.current):
                            self.current.move(0, -1)
                    elif event.key == pygame.K_UP:
                        self.current.rotate()
                        if not self.grid.is_valid(self.current):
                            self.current.rotate()
                            self.current.rotate()
                            self.current.rotate()

    def update(self):
        """게임 업데이트"""
        if self.game_over:
            return

        self.fall_time += 1
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            self.current.move(0, 1)

            if not self.grid.is_valid(self.current):
                self.current.move(0, -1)
                self.grid.place(self.current)

                lines = self.grid.clear_lines()
                self.score += lines * 100
                self.level = 1 + self.score // 500
                self.fall_speed = max(5, 30 - self.level * 2)

                self.current = Tetromino()
                if not self.grid.is_valid(self.current):
                    self.game_over = True

    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)

        # 그리드 그리기
        self.grid.draw(self.screen)

        # 현재 테트로미노 그리기
        if not self.game_over:
            for x, y in self.current.get_cells():
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, self.current.color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)

        # 점수 표시
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT + 10))
        self.screen.blit(level_text, (200, SCREEN_HEIGHT + 10))

        # 게임 오버
        if self.game_over:
            game_over_text = pygame.font.Font(None, 72).render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    def run(self):
        """게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
