#!/usr/bin/env python3
"""
Tetris - 상세 구현
클래식 퍼즐 게임: 떨어지는 블록을 정렬해 행을 완성
"""
import pygame
import random
from enum import Enum
from graphics_themes import Color, Themes

class TetrisShape(Enum):
    """테트리스 블록 모양"""
    I = 0      # 일자
    O = 1      # 정사각형
    T = 2      # T자
    S = 3      # S자
    Z = 4      # Z자
    J = 5      # J자
    L = 6      # L자

class TetrisBlock:
    """테트리스 블록"""

    # 블록 모양 정의 (4x4 그리드)
    SHAPES = {
        TetrisShape.I: [[1, 1, 1, 1]],
        TetrisShape.O: [[1, 1], [1, 1]],
        TetrisShape.T: [[0, 1, 0], [1, 1, 1]],
        TetrisShape.S: [[0, 1, 1], [1, 1, 0]],
        TetrisShape.Z: [[1, 1, 0], [0, 1, 1]],
        TetrisShape.J: [[1, 0, 0], [1, 1, 1]],
        TetrisShape.L: [[0, 0, 1], [1, 1, 1]]
    }

    COLORS = {
        TetrisShape.I: Color.CYAN,
        TetrisShape.O: Color.YELLOW,
        TetrisShape.T: Color.MAGENTA,
        TetrisShape.S: Color.GREEN,
        TetrisShape.Z: Color.RED,
        TetrisShape.J: Color.BLUE,
        TetrisShape.L: (255, 165, 0)  # 오렌지
    }

    def __init__(self, shape=None):
        if shape is None:
            shape = random.choice(list(TetrisShape))
        self.shape = shape
        self.grid = self.SHAPES[shape]
        self.color = self.COLORS[shape]
        self.x = 3  # 열
        self.y = 0  # 행
        self.rotation = 0

    def get_grid(self):
        """현재 회전 상태의 그리드"""
        return self.grid

    def rotate(self):
        """블록 회전"""
        # 간단한 90도 회전
        h = len(self.grid)
        w = len(self.grid[0]) if h > 0 else 0

        new_grid = [[0] * h for _ in range(w)]
        for i in range(h):
            for j in range(w):
                new_grid[j][h - 1 - i] = self.grid[i][j]

        self.grid = new_grid
        self.rotation = (self.rotation + 1) % 4


class TetrisGame:
    """Tetris 상세 구현"""

    def __init__(self):
        pygame.init()

        self.window_width = 400
        self.window_height = 600
        self.game_name = "Tetris"

        # 게임 판
        self.grid_width = 10
        self.grid_height = 20
        self.block_size = 25
        self.board = [[0] * self.grid_width for _ in range(self.grid_height)]

        # 게임 상태
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False

        # 현재 블록
        self.current_block = TetrisBlock()
        self.next_block = TetrisBlock()

        # 타이밍
        self.fall_time = 0
        self.fall_speed = 500  # ms

        # 테마
        self.theme = Themes.NEON

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.game_name)

        self.running = True

    def _can_place_block(self, block, x, y):
        """블록을 배치할 수 있는지 확인"""
        for i, row in enumerate(block.get_grid()):
            for j, cell in enumerate(row):
                if cell:
                    board_x = x + j
                    board_y = y + i

                    # 경계 확인
                    if board_x < 0 or board_x >= self.grid_width:
                        return False
                    if board_y < 0 or board_y >= self.grid_height:
                        return False

                    # 충돌 확인
                    if self.board[board_y][board_x]:
                        return False

        return True

    def _place_block(self, block):
        """블록을 보드에 배치"""
        for i, row in enumerate(block.get_grid()):
            for j, cell in enumerate(row):
                if cell:
                    board_x = block.x + j
                    board_y = block.y + i

                    if 0 <= board_y < self.grid_height and 0 <= board_x < self.grid_width:
                        self.board[board_y][board_x] = block.color

    def _clear_lines(self):
        """완전한 행 제거"""
        rows_to_remove = []

        for i, row in enumerate(self.board):
            if all(row):
                rows_to_remove.append(i)

        for row_index in reversed(rows_to_remove):
            del self.board[row_index]
            self.board.insert(0, [0] * self.grid_width)

        cleared = len(rows_to_remove)
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += cleared * 100
            self.level = 1 + (self.lines_cleared // 10)
            self.fall_speed = max(100, 500 - (self.level * 50))

    def _handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    if self._can_place_block(self.current_block, self.current_block.x - 1, self.current_block.y):
                        self.current_block.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if self._can_place_block(self.current_block, self.current_block.x + 1, self.current_block.y):
                        self.current_block.x += 1
                elif event.key == pygame.K_DOWN:
                    if self._can_place_block(self.current_block, self.current_block.x, self.current_block.y + 1):
                        self.current_block.y += 1
                    else:
                        self._place_block(self.current_block)
                        self._clear_lines()
                        self.current_block = self.next_block
                        self.next_block = TetrisBlock()
                        if not self._can_place_block(self.current_block, self.current_block.x, self.current_block.y):
                            self.game_over = True
                elif event.key == pygame.K_UP:
                    old_rotation = self.current_block.rotation
                    self.current_block.rotate()
                    if not self._can_place_block(self.current_block, self.current_block.x, self.current_block.y):
                        self.current_block.rotation = old_rotation
                        self.current_block.grid = TetrisBlock.SHAPES[self.current_block.shape]

    def _update(self, dt):
        """게임 업데이트"""
        if self.game_over:
            return

        self.fall_time += dt

        if self.fall_time >= self.fall_speed:
            self.fall_time = 0

            if self._can_place_block(self.current_block, self.current_block.x, self.current_block.y + 1):
                self.current_block.y += 1
            else:
                self._place_block(self.current_block)
                self._clear_lines()
                self.current_block = self.next_block
                self.next_block = TetrisBlock()

                if not self._can_place_block(self.current_block, self.current_block.x, self.current_block.y):
                    self.game_over = True

    def _draw(self, surface):
        """화면 그리기"""
        surface.fill(self.theme.bg_color)

        # 게임 판 그리기
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(x * self.block_size, y * self.block_size,
                                  self.block_size, self.block_size)

                if self.board[y][x]:
                    pygame.draw.rect(surface, self.board[y][x], rect)
                pygame.draw.rect(surface, self.theme.secondary_color, rect, 1)

        # 현재 블록 그리기
        for i, row in enumerate(self.current_block.get_grid()):
            for j, cell in enumerate(row):
                if cell:
                    x = (self.current_block.x + j) * self.block_size
                    y = (self.current_block.y + i) * self.block_size
                    rect = pygame.Rect(x, y, self.block_size, self.block_size)
                    pygame.draw.rect(surface, self.current_block.color, rect)
                    pygame.draw.rect(surface, Color.WHITE, rect, 1)

        # 점수 표시
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, self.theme.primary_color)
        level_text = font.render(f"Level: {self.level}", True, self.theme.primary_color)
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, self.theme.primary_color)

        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 35))
        surface.blit(lines_text, (10, 60))

        # 게임 오버
        if self.game_over:
            font_large = pygame.font.Font(None, 60)
            go_text = font_large.render("GAME OVER", True, Color.RED)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            surface.blit(go_text, go_rect)

    def run(self):
        """게임 실행"""
        while self.running:
            self._handle_input()
            dt = self.clock.tick(60)
            self._update(dt)
            self._draw(self.display)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
