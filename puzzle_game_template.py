#!/usr/bin/env python3
"""
🧩 퍼즐 게임 템플릿
Tetris, Sokoban, Sudoku 등 퍼즐 게임의 기본 구현
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from game_utils import ScoreManager, GameConfig, GameState
from sound_manager import SoundManager
from graphics_themes import Themes, Color

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
GRID_SIZE = 20

class PuzzleGame:
    """퍼즐 게임 기본 클래스"""
    def __init__(self, game_name):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"🧩 {game_name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 매니저
        self.score_manager = ScoreManager(game_name.lower().replace(" ", "_"))
        self.config = GameConfig(game_name.lower().replace(" ", "_"))
        self.sound_manager = SoundManager()
        self.game_state = GameState()

        # 테마
        theme_name = self.config.get("theme", "classic")
        self.theme = getattr(Themes, theme_name.upper(), Themes.CLASSIC)

        # 게임 상태
        self.running = True
        self.paused = False
        self.score = 0
        self.level = 1
        self.moves = 0
        self.hint_available = 3

        # 그리드 (20x20)
        self.grid_width = 10
        self.grid_height = 15
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.selected_pieces = []

    def handle_input(self, keys):
        """입력 처리 (오버라이드 필요)"""
        pass

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_h:
                    self._use_hint()
                elif event.key == pygame.K_z:  # 실행 취소
                    self._undo()
                elif event.key == pygame.K_SPACE:
                    self._restart()
                self.handle_input(pygame.key.get_pressed())

    def _use_hint(self):
        """힌트 사용"""
        if self.hint_available > 0:
            self.hint_available -= 1
            print(f"힌트 남음: {self.hint_available}")

    def _undo(self):
        """실행 취소"""
        self.moves = max(0, self.moves - 1)

    def _restart(self):
        """다시 시작"""
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.moves = 0
        self.score = 0

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        # 각 게임에서 구현

    def _check_win(self):
        """승리 조건 체크 (오버라이드 필요)"""
        return False

    def draw_grid(self):
        """그리드 그리기"""
        grid_x = 50
        grid_y = 100
        cell_size = 30

        # 그리드 배경
        grid_rect = pygame.Rect(grid_x, grid_y,
                                self.grid_width * cell_size,
                                self.grid_height * cell_size)
        pygame.draw.rect(self.screen, self.theme.secondary_color, grid_rect, 2)

        # 그리드 셀
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_x = grid_x + x * cell_size
                cell_y = grid_y + y * cell_size
                cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)

                if self.grid[y][x] > 0:
                    pygame.draw.rect(self.screen, self.theme.primary_color, cell_rect)
                else:
                    pygame.draw.rect(self.screen, self.theme.bg_color, cell_rect, 1)

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 제목
        title_text = self.font.render("Puzzle Game", True, self.theme.text_color)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 100, 20))

        # 그리드 그리기
        self.draw_grid()

        # 정보 표시
        info_y = 50
        score_text = self.small_font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, info_y))

        level_text = self.small_font.render(f"Level: {self.level}", True, self.theme.text_color)
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, info_y + 30))

        moves_text = self.small_font.render(f"Moves: {self.moves}", True, self.theme.text_color)
        self.screen.blit(moves_text, (SCREEN_WIDTH - 200, info_y + 60))

        hint_text = self.small_font.render(f"Hints: {self.hint_available}", True, self.theme.text_color)
        self.screen.blit(hint_text, (SCREEN_WIDTH - 200, info_y + 90))

        # 컨트롤 정보
        controls = [
            "SPACE: Restart",
            "Z: Undo",
            "H: Hint",
            "P: Pause"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, self.theme.text_color)
            self.screen.blit(control_text, (10, SCREEN_HEIGHT - 100 + i * 25))

        # 일시정지
        if self.paused:
            pause_text = self.font.render("PAUSED", True, Color.RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        """게임 실행"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # 점수 저장
        if self.score > 0:
            rank = self.score_manager.add_score(
                self.config.get("player_name", "Player"),
                self.score
            )

        pygame.quit()
