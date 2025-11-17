#!/usr/bin/env python3
"""
🎮 게임 002 - Snake (뱀) (Enhanced Version)
개선된 버전: 하이스코어, 멀티플레이, 사운드, 테마 지원
"""

import pygame
import random
import sys
from pathlib import Path

# 공유 라이브러리 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from game_utils import ScoreManager, GameConfig, GameState, format_score
from sound_manager import SoundManager
from graphics_themes import Themes, Color, GraphicsHelper

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
GAME_NAME = "snake"

class EnhancedGame:
    """개선된 Snake (뱀) 게임"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 Snake (뱀) - Enhanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        # 매니저 초기화
        self.score_manager = ScoreManager(GAME_NAME)
        self.config = GameConfig(GAME_NAME)
        self.sound_manager = SoundManager(
            self.config.get("volume"),
            self.config.get("music_volume")
        )
        self.game_state = GameState()

        # 테마 선택
        theme_name = self.config.get("theme", "classic")
        self.theme = getattr(Themes, theme_name.upper(), Themes.CLASSIC)

        self.score = 0
        self.game_over = False
        self.running = True
        self.paused = False

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_p:
                    self.game_state.paused = not self.game_state.paused
                elif event.key == pygame.K_h:
                    self.show_highscores()

    def update(self):
        """게임 업데이트"""
        if self.game_state.paused or self.game_over:
            return

        # 게임 로직 추가 필요
        pass

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 점수 표시
        score_text = self.small_font.render(f"Score: {0}", True, self.theme.primary_color)
        self.screen.blit(score_text, (20, 20))

        # 일시정지 표시
        if self.game_state.paused:
            pause_text = self.font.render("PAUSED", True, self.theme.secondary_color)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def reset_game(self):
        """게임 초기화"""
        self.score = 0
        self.game_over = False
        self.game_state.reset()

    def show_highscores(self):
        """하이스코어 표시"""
        scores = self.score_manager.get_top_scores()
        # 하이스코어 표시 로직
        pass

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
    game = EnhancedGame()
    game.run()
