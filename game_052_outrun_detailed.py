#!/usr/bin/env python3
"""🏎️ OutRun (게임 052) - 열대 레이싱"""
import pygame, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from racing_game_template import RacingGame, RacingCar
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class OutRunGame(RacingGame):
    """OutRun 레이싱 게임"""
    def __init__(self):
        super().__init__("OutRun")
        self.player.max_speed = 18
        self.time_limit = 120 * 60  # 2분
        self.scenic_mode = 0  # 배경 변경
        self.traffic_cars = []

    def update(self):
        if self.paused or self.game_state.game_over:
            return
        self.time_limit -= 1
        self.time_elapsed += 1
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.player.speed = min(self.player.max_speed, self.player.speed + self.player.acceleration)
        if keys[pygame.K_DOWN]:
            self.player.speed = max(-5, self.player.speed - self.player.acceleration)
        if keys[pygame.K_LEFT]:
            self.player.x = max(0, self.player.x - 3)
        if keys[pygame.K_RIGHT]:
            self.player.x = min(SCREEN_WIDTH - self.player.width, self.player.x + 3)
        
        self.player.speed *= self.player.friction
        self.player.distance += self.player.speed
        self.score = int(self.player.distance)
        
        if self.time_limit <= 0 or self.player.lap >= self.laps_to_win:
            self.game_state.game_over = True

    def draw(self):
        # 배경 (열대 테마)
        if self.score < 5000:
            self.screen.fill((0, 100, 200))  # 파란 하늘
        elif self.score < 10000:
            self.screen.fill((200, 100, 50))  # 석양
        else:
            self.screen.fill((50, 50, 100))  # 밤
        
        # 도로
        pygame.draw.rect(self.screen, (150, 150, 150), (100, 300, 600, 100))
        
        # 플레이어 차
        pygame.draw.rect(self.screen, (255, 0, 0), (self.player.x, 450, 30, 40))
        
        # UI
        speed_text = self.font.render(f"Speed: {int(self.player.speed)}", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 10))
        
        dist_text = self.font.render(f"Distance: {self.score}", True, (255, 255, 255))
        self.screen.blit(dist_text, (10, 50))
        
        time_text = self.small_font.render(f"Time: {self.time_limit // 60}s", True, (255, 255, 255))
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 10))
        
        if self.game_state.game_over:
            over = self.font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(over, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = OutRunGame()
    game.run()
