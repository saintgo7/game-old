#!/usr/bin/env python3
"""
🏎️ 레이싱 게임 템플릿
Formula1, OutRun, MarioKart 등 레이싱 게임의 기본 구현
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

class RacingCar:
    """레이싱 자동차"""
    def __init__(self, x, y, is_player=False):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.speed = 0
        self.max_speed = 15
        self.acceleration = 0.3
        self.friction = 0.95
        self.rotation = 0
        self.is_player = is_player
        self.lap = 0
        self.distance = 0

    def update(self, keys=None):
        """업데이트"""
        if self.is_player and keys:
            if keys[pygame.K_UP]:
                self.speed = min(self.max_speed, self.speed + self.acceleration)
            if keys[pygame.K_DOWN]:
                self.speed = max(-self.max_speed / 2, self.speed - self.acceleration)
            if keys[pygame.K_LEFT]:
                self.rotation = (self.rotation - 5) % 360
            if keys[pygame.K_RIGHT]:
                self.rotation = (self.rotation + 5) % 360
        else:
            # AI 자동차
            self.speed = min(self.max_speed * 0.8, self.speed + self.acceleration * 0.5)

        # 속도 적용
        self.speed *= self.friction
        move_x = self.speed * pygame.math.Vector2(1, 0).rotate(self.rotation).x
        move_y = self.speed * pygame.math.Vector2(1, 0).rotate(self.rotation).y

        self.x += move_x
        self.y += move_y
        self.distance += abs(self.speed)

        # 경계 체크
        if self.x < 0:
            self.x = 0
            self.speed *= -0.5
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.speed *= -0.5
        if self.y < 0:
            self.y = 0
            self.speed *= -0.5
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.speed *= -0.5

    def draw(self, surface, color):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rect)
        # 방향 표시선
        end_x = self.x + self.width // 2 + 20 * pygame.math.Vector2(1, 0).rotate(self.rotation).x
        end_y = self.y + self.height // 2 + 20 * pygame.math.Vector2(1, 0).rotate(self.rotation).y
        pygame.draw.line(surface, Color.WHITE, (self.x + self.width // 2, self.y + self.height // 2),
                        (end_x, end_y), 2)

class RacingGame:
    """레이싱 게임 기본 클래스"""
    def __init__(self, game_name):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"🏎️ {game_name}")
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
        self.time_elapsed = 0
        self.laps_to_win = 3

        # 플레이어 자동차
        self.player = RacingCar(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, is_player=True)

        # 상대 자동차
        self.opponents = [
            RacingCar(SCREEN_WIDTH // 2 - 100, 100),
            RacingCar(SCREEN_WIDTH // 2 + 100, 150),
        ]

        # 트랙 체크포인트
        self.checkpoints = [
            (SCREEN_WIDTH // 2, 50),     # 시작선
            (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50),
            (100, SCREEN_HEIGHT // 2),
        ]
        self.current_checkpoint = 0

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
                elif event.key == pygame.K_SPACE:
                    self._restart()

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        self.time_elapsed += 1

        # 플레이어 입력
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        # 상대 자동차 업데이트
        for opponent in self.opponents:
            opponent.update()

        # 체크포인트 체크
        self._check_checkpoints()

        # 충돌 체크
        self._check_collisions()

        # 점수 계산
        self.score = int(self.player.distance)

    def _check_checkpoints(self):
        """체크포인트 체크"""
        checkpoint = self.checkpoints[self.current_checkpoint]
        dist = ((self.player.x - checkpoint[0])**2 + (self.player.y - checkpoint[1])**2)**0.5

        if dist < 50:
            self.current_checkpoint = (self.current_checkpoint + 1) % len(self.checkpoints)
            if self.current_checkpoint == 0:
                self.player.lap += 1
                if self.player.lap >= self.laps_to_win:
                    self.game_state.game_over = True

    def _check_collisions(self):
        """충돌 체크"""
        for opponent in self.opponents:
            dist = ((self.player.x - opponent.x)**2 + (self.player.y - opponent.y)**2)**0.5
            if dist < 40:
                self.player.speed *= -0.5
                opponent.speed *= -0.5

    def _restart(self):
        """다시 시작"""
        self.player = RacingCar(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, is_player=True)
        self.opponents = [
            RacingCar(SCREEN_WIDTH // 2 - 100, 100),
            RacingCar(SCREEN_WIDTH // 2 + 100, 150),
        ]
        self.time_elapsed = 0
        self.score = 0

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 트랙 그리기
        pygame.draw.rect(self.screen, Color.GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

        # 체크포인트 그리기
        for i, checkpoint in enumerate(self.checkpoints):
            color = Color.GREEN if i == self.current_checkpoint else Color.YELLOW
            pygame.draw.circle(self.screen, color, checkpoint, 30, 2)

        # 자동차 그리기
        self.player.draw(self.screen, Color.BLUE)
        for i, opponent in enumerate(self.opponents):
            color = Color.RED if i == 0 else Color.YELLOW
            opponent.draw(self.screen, color)

        # UI
        score_text = self.font.render(f"Distance: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (10, 10))

        lap_text = self.font.render(f"Lap: {self.player.lap}/{self.laps_to_win}", True, self.theme.text_color)
        self.screen.blit(lap_text, (10, 50))

        speed_text = self.small_font.render(f"Speed: {self.player.speed:.1f}", True, self.theme.text_color)
        self.screen.blit(speed_text, (10, 90))

        time_text = self.small_font.render(f"Time: {self.time_elapsed // 60}s", True, self.theme.text_color)
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

        # 게임 오버
        if self.game_state.game_over:
            finish_text = self.font.render("FINISHED!", True, Color.GREEN)
            self.screen.blit(finish_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

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
