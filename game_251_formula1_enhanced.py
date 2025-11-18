#!/usr/bin/env python3
"""
🏎️ Formula 1 (게임 251) - 상세 구현
고급 레이싱 게임으로, 플레이어가 포뮬러1 경주차를 조종하여
최고의 성능으로 트랙을 완성
"""

import pygame
import random
import sys
from pathlib import Path
import math

sys.path.insert(0, str(Path(__file__).parent))

from racing_game_template import RacingGame, RacingCar
from graphics_themes import Color

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Formula1Game(RacingGame):
    """Formula1 게임 - 레이싱 템플릿 확장"""

    def __init__(self):
        super().__init__("Formula 1")

        # F1 특화 설정
        self.player.max_speed = 20
        self.player.acceleration = 0.5
        self.player.friction = 0.92

        # 상대 자동차
        self.opponents = [
            RacingCar(SCREEN_WIDTH // 2 - 100, 50),
            RacingCar(SCREEN_WIDTH // 2 + 100, 70),
        ]

        for opponent in self.opponents:
            opponent.max_speed = 18
            opponent.acceleration = 0.4
            opponent.friction = 0.93

        # F1 특화
        self.best_lap_time = float('inf')
        self.lap_times = []
        self.lap_start_time = self.time_elapsed
        self.pit_stop_needed = False
        self.fuel = 100
        self.max_fuel = 100
        self.tire_wear = 0
        self.max_tire_wear = 100

    def update(self):
        """Formula1 특화: 연료, 타이어 마모 시뮬레이션"""
        if self.paused or self.game_state.game_over:
            return

        self.time_elapsed += 1

        # 연료 소비
        self.fuel -= abs(self.player.speed) * 0.01
        if self.fuel <= 0:
            self.player.max_speed = 5  # 기력 소진

        # 타이어 마모
        self.tire_wear += abs(self.player.speed) * 0.02
        if self.tire_wear > self.max_tire_wear:
            self.player.max_speed = max(8, 20 - (self.tire_wear - self.max_tire_wear) * 0.1)

        # 기본 업데이트
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        for opponent in self.opponents:
            opponent.update()

        # 체크포인트 체크
        self._check_checkpoints()

        # 충돌 체크
        self._check_collisions()

        # 점수 계산
        self.score = int(self.player.distance)

        # 라운드 종료
        if self.player.lap >= self.laps_to_win:
            lap_time = self.time_elapsed - self.lap_start_time
            self.lap_times.append(lap_time)
            if lap_time < self.best_lap_time:
                self.best_lap_time = lap_time
            self.game_state.game_over = True

    def _check_checkpoints(self):
        """체크포인트 체크 (F1 특화)"""
        checkpoint = self.checkpoints[self.current_checkpoint]
        dist = ((self.player.x - checkpoint[0])**2 + (self.player.y - checkpoint[1])**2)**0.5

        if dist < 50:
            self.current_checkpoint = (self.current_checkpoint + 1) % len(self.checkpoints)
            if self.current_checkpoint == 0:
                self.player.lap += 1
                lap_time = self.time_elapsed - self.lap_start_time
                self.lap_times.append(lap_time)
                if lap_time < self.best_lap_time:
                    self.best_lap_time = lap_time
                self.lap_start_time = self.time_elapsed

    def draw(self):
        """Formula1 특화: 성능 지표 표시"""
        super().draw()

        # 연료 게이지
        fuel_ratio = max(0, self.fuel / self.max_fuel)
        pygame.draw.rect(self.screen, Color.RED, (10, SCREEN_HEIGHT - 80, 150, 20))
        pygame.draw.rect(self.screen, Color.GREEN, (10, SCREEN_HEIGHT - 80, 150 * fuel_ratio, 20))
        pygame.draw.rect(self.screen, Color.WHITE, (10, SCREEN_HEIGHT - 80, 150, 20), 2)
        fuel_text = self.small_font.render(f"Fuel: {int(self.fuel)}", True, self.theme.text_color)
        self.screen.blit(fuel_text, (10, SCREEN_HEIGHT - 110))

        # 타이어 마모
        tire_ratio = self.tire_wear / self.max_tire_wear
        pygame.draw.rect(self.screen, Color.RED, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 80, 150, 20))
        pygame.draw.rect(self.screen, Color.YELLOW, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 80, 150 * tire_ratio, 20))
        pygame.draw.rect(self.screen, Color.WHITE, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 80, 150, 20), 2)
        tire_text = self.small_font.render(f"Tires: {int(100 - min(100, self.tire_wear))}%", True, self.theme.text_color)
        self.screen.blit(tire_text, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 110))

        # 최고 랩타임
        if self.best_lap_time != float('inf'):
            best_time = self.best_lap_time // 60
            best_ms = (self.best_lap_time % 60) * 100 // 60
            best_text = self.small_font.render(f"Best Lap: {int(best_time)}:{int(best_ms):02d}", True, Color.YELLOW)
            self.screen.blit(best_text, (SCREEN_WIDTH // 2 - 80, 10))

if __name__ == "__main__":
    game = Formula1Game()
    game.run()
