#!/usr/bin/env python3
"""
🔫 슈팅 게임 템플릿
Defender, Phoenix, Galaga 등 슈팅 게임의 기본 구현
"""

import pygame
import random
import sys
from pathlib import Path
from enum import Enum

# 공유 라이브러리 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from game_utils import ScoreManager, GameConfig, GameState, Difficulty
from sound_manager import SoundManager
from graphics_themes import Themes, Color, GraphicsHelper

pygame.init()

# 게임 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class GameDifficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4

class Player:
    """플레이어 캐릭터"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = 5
        self.health = 100
        self.bullets = []
        self.fire_rate = 10
        self.fire_cooldown = 0

    def handle_input(self, keys):
        """입력 처리"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        """발사"""
        if self.fire_cooldown <= 0:
            self.bullets.append(Bullet(self.x + self.width // 2, self.y))
            self.fire_cooldown = self.fire_rate

    def update(self):
        """업데이트"""
        self.fire_cooldown -= 1
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, theme.primary_color, rect)

class Enemy:
    """적 캐릭터"""
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = 2
        self.health = 10
        self.fire_rate = 30
        self.fire_cooldown = random.randint(0, 30)
        self.bullets = []
        self.type = enemy_type

    def update(self):
        """업데이트"""
        # 좌우 움직임
        self.x += self.speed
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.speed *= -1

        # 발사
        self.fire_cooldown -= 1
        if self.fire_cooldown <= 0:
            self.bullets.append(EnemyBullet(self.x, self.y))
            self.fire_cooldown = self.fire_rate

        # 총알 업데이트
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, theme.secondary_color, rect)

class Bullet:
    """플레이어 총알"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 15
        self.speed = 7

    def update(self):
        self.y -= self.speed

    def draw(self, surface, color):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rect)

class EnemyBullet:
    """적 총알"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.speed = 4

    def update(self):
        self.y += self.speed

    def draw(self, surface, color):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, rect)

class ShootingGame:
    """슈팅 게임 기본 클래스"""
    def __init__(self, game_name, difficulty=GameDifficulty.NORMAL):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"🔫 {game_name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # 매니저 초기화
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
        self.difficulty = difficulty

        # 게임 오브젝트
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.enemies = []
        self.wave = 1
        self.wave_enemy_count = 5 + self.wave
        self.score = 0
        self.level = 1

        self._spawn_enemies()

    def _spawn_enemies(self):
        """적 생성"""
        for i in range(self.wave_enemy_count):
            x = random.randint(0, SCREEN_WIDTH - 25)
            y = random.randint(20, 150)
            self.enemies.append(Enemy(x, y))

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
                    self._show_highscores()

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        # 플레이어 입력
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()

        # 적 업데이트
        for enemy in self.enemies[:]:
            enemy.update()

        # 충돌 검사
        self._check_collisions()

        # 웨이브 체크
        if len(self.enemies) == 0:
            self.wave += 1
            self.level += 1
            self.wave_enemy_count += 2
            self._spawn_enemies()

    def _check_collisions(self):
        """충돌 검사"""
        # 플레이어 총알 vs 적
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if self._rect_collision(
                    bullet.x, bullet.y, bullet.width, bullet.height,
                    enemy.x, enemy.y, enemy.width, enemy.height
                ):
                    self.score += 100
                    self.player.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

        # 적 총알 vs 플레이어
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if self._rect_collision(
                    bullet.x, bullet.y, bullet.width, bullet.height,
                    self.player.x, self.player.y, self.player.width, self.player.height
                ):
                    self.player.health -= 10
                    enemy.bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.game_state.game_over = True

    def _rect_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        """사각형 충돌 검사"""
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def _show_highscores(self):
        """하이스코어 표시"""
        scores = self.score_manager.get_top_scores()
        # 간단한 표시 (실제로는 UI 개선)
        print("=== 하이스코어 ===")
        for i, score in enumerate(scores[:5], 1):
            print(f"{i}. {score['name']}: {score['score']}")

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 플레이어 그리기
        self.player.draw(self.screen, self.theme)

        # 플레이어 총알 그리기
        for bullet in self.player.bullets:
            bullet.draw(self.screen, Color.YELLOW)

        # 적 그리기
        for enemy in self.enemies:
            enemy.draw(self.screen, self.theme)
            for bullet in enemy.bullets:
                bullet.draw(self.screen, Color.RED)

        # UI 그리기
        score_text = self.font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (10, 10))

        health_text = self.font.render(f"Health: {self.player.health}", True, self.theme.text_color)
        self.screen.blit(health_text, (10, 50))

        level_text = self.font.render(f"Wave: {self.wave}", True, self.theme.text_color)
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 10))

        # 일시정지 표시
        if self.paused:
            pause_text = self.font.render("PAUSED", True, Color.RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # 게임 오버
        if self.game_state.game_over:
            over_text = self.font.render("GAME OVER", True, Color.RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            final_score = self.small_font.render(f"Final Score: {self.score}", True, self.theme.text_color)
            self.screen.blit(final_score, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50))

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
