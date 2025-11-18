#!/usr/bin/env python3
"""
🚀 Galaga (게임 463) - 상세 구현
클래식 슈팅게임의 대표작으로, 적들의 포메이션 비행, 특수 공격, 파워업 시스템 포함
"""

import pygame
import random
import math
import sys
from pathlib import Path
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent))

from shooting_game_template import ShootingGame, GameDifficulty, Player, Enemy, Bullet, EnemyBullet
from graphics_themes import Color

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class FormationPattern(Enum):
    """포메이션 패턴"""
    LINE = 1        # 일렬 진형
    V_SHAPE = 2     # V자 진형
    WAVE = 3        # 파도 진형
    CIRCLE = 4      # 원형 진형
    SPIRAL = 5      # 나선형 진형

class PowerUp:
    """파워업 아이템"""
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.power_type = power_type  # "rapid", "dual", "bomb", "shield"
        self.speed = 2
        self.active = True

    def update(self):
        """업데이트"""
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, surface, color_map):
        """그리기"""
        colors = {
            "rapid": Color.YELLOW,
            "dual": Color.GREEN,
            "bomb": Color.RED,
            "shield": Color.CYAN
        }
        color = colors.get(self.power_type, Color.WHITE)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, Color.WHITE, (self.x, self.y, self.width, self.height), 1)

class GalagaEnemy(Enemy):
    """갈라가 적"""
    def __init__(self, x, y, enemy_type=1):
        super().__init__(x, y, enemy_type)
        self.formation_x = x
        self.formation_y = y
        self.formation_offset = 0
        self.formation_speed = 2
        self.dive_target = None
        self.is_diving = False
        self.capture_mode = False
        self.movement_phase = 0

    def set_formation(self, pattern, offset):
        """포메이션 설정"""
        self.movement_phase = pattern
        self.formation_offset = offset

    def update_formation(self, time):
        """포메이션 이동"""
        if not self.is_diving:
            if self.movement_phase == FormationPattern.WAVE.value:
                # 파도 패턴
                self.x = self.formation_x + math.sin(time * 0.05 + self.formation_offset) * 50
                self.y = self.formation_y + abs(math.cos(time * 0.03)) * 20
            elif self.movement_phase == FormationPattern.SPIRAL.value:
                # 나선형 패턴
                radius = 30 + time * 0.2
                angle = time * 0.1 + self.formation_offset
                self.x = self.formation_x + radius * math.cos(angle)
                self.y = self.formation_y + radius * math.sin(angle)
            elif self.movement_phase == FormationPattern.LINE.value:
                # 일렬 진형
                self.x = self.formation_x + self.formation_offset
                self.y = self.formation_y

    def start_dive(self, target_x):
        """다이브 공격 시작"""
        self.is_diving = True
        self.dive_target = target_x
        self.dive_speed = 4

    def dive_update(self):
        """다이브 이동"""
        if self.is_diving and self.dive_target:
            # 대상을 향해 이동
            if abs(self.x - self.dive_target) > 10:
                direction = 1 if self.dive_target > self.x else -1
                self.x += direction * self.dive_speed
                self.y += self.dive_speed * 2
            else:
                self.is_diving = False

class GalagaGame(ShootingGame):
    """Galaga - 갈라가 게임 (상세 구현)"""

    def __init__(self):
        super().__init__("Galaga", difficulty=GameDifficulty.NORMAL)

        # Galaga 특화 설정
        self.player.max_speed = 5
        self.player.fire_rate = 10

        # 포메이션 시스템
        self.formation_pattern = FormationPattern.WAVE
        self.time_counter = 0
        self.formation_x = SCREEN_WIDTH // 2
        self.formation_y = 50

        # 파워업
        self.power_ups = []
        self.dual_fire = False
        self.dual_timer = 0
        self.rapid_fire = False
        self.rapid_timer = 0
        self.shield = False
        self.shield_health = 0

        # 스테이지
        self.stage = 1
        self.enemies_per_stage = 3
        self.enemy_speed = 2

        # Hawk 공격 (특수 기능)
        self.hawk_available = False
        self.hawk_cooldown = 0
        self.hawk_max_cooldown = 300  # 5초

        # 캡처 시스템
        self.captured_enemies = []
        self.capture_timer = 0

        # 추가 점수
        self.stage_clear_bonus = 0

    def _spawn_enemies(self):
        """포메이션 이동하는 적 생성"""
        self.enemies = []
        enemies_per_row = 4
        rows = (self.enemies_per_stage * self.stage) // enemies_per_row + 1

        for row in range(min(rows, 3)):  # 최대 3열
            for col in range(enemies_per_row):
                if len(self.enemies) >= self.enemies_per_stage * self.stage:
                    break

                x = 100 + col * 150
                y = 50 + row * 60
                enemy = GalagaEnemy(x, y, 1 + (row % 2))
                enemy.set_formation(self.formation_pattern.value, col * 20 + row * 10)
                enemy.speed = self.enemy_speed
                self.enemies.append(enemy)

    def update(self):
        """Galaga 특화 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        self.time_counter += 1

        # 플레이어 입력
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Hawk 공격 (스페이스바)
        if keys[pygame.K_SPACE] and self.hawk_available and self.hawk_cooldown <= 0:
            self._perform_hawk_attack()
            self.hawk_cooldown = self.hawk_max_cooldown
            self.hawk_available = False

        # 플레이어 업데이트
        self.player.update()

        # 파워업 업데이트
        for powerup in self.power_ups[:]:
            powerup.update()
            if not powerup.active:
                self.power_ups.remove(powerup)
            else:
                # 플레이어와 충돌
                if self._rect_collision(
                    powerup.x, powerup.y, powerup.width, powerup.height,
                    self.player.x, self.player.y, self.player.width, self.player.height
                ):
                    self._apply_powerup(powerup.power_type)
                    self.power_ups.remove(powerup)

        # 적 업데이트 (포메이션 이동)
        for enemy in self.enemies[:]:
            if isinstance(enemy, GalagaEnemy):
                enemy.update_formation(self.time_counter)
                if enemy.is_diving:
                    enemy.dive_update()

                # 무작위 다이브 공격
                if random.random() < 0.002 and not enemy.is_diving:
                    enemy.start_dive(self.player.x)

                # 적 발사
                if random.random() < (0.005 + self.wave * 0.001):
                    enemy_bullet = EnemyBullet(enemy.x, enemy.y)
                    enemy.bullets.append(enemy_bullet)
            else:
                enemy.update()

        # 쿨다운 감소
        self.hawk_cooldown = max(0, self.hawk_cooldown - 1)
        self.dual_timer = max(0, self.dual_timer - 1)
        self.rapid_timer = max(0, self.rapid_timer - 1)

        # 파워업 활성화 토글
        if self.dual_timer == 0:
            self.dual_fire = False
        if self.rapid_timer == 0:
            self.rapid_fire = False

        # 충돌 검사
        self._check_collisions()

        # 방어막 체크
        if not self.shield and self.shield_health > 0:
            self.shield = True

        # 웨이브 진행
        if len(self.enemies) == 0:
            self.wave += 1
            self.stage += 1
            self.enemies_per_stage = 3 + self.stage
            self.enemy_speed = min(6, 2 + self.stage * 0.3)
            self.formation_pattern = FormationPattern(1 + (self.stage % 5))
            self._spawn_enemies()
            self.stage_clear_bonus = 1000 * self.stage
            self.score += self.stage_clear_bonus
            self.hawk_available = True

    def _perform_hawk_attack(self):
        """Hawk 공격 (특수 기능)"""
        # 모든 적에게 피해
        for enemy in self.enemies:
            enemy.health = 0
        self.score += len(self.enemies) * 100

    def _apply_powerup(self, power_type):
        """파워업 적용"""
        if power_type == "rapid":
            self.rapid_fire = True
            self.rapid_timer = 300  # 5초
            self.player.fire_rate = 5
        elif power_type == "dual":
            self.dual_fire = True
            self.dual_timer = 300
        elif power_type == "bomb":
            # 모든 적 제거
            bomb_damage = len(self.enemies) * 50
            self.enemies = []
            self.score += bomb_damage
        elif power_type == "shield":
            self.shield = True
            self.shield_health = 100

    def _check_collisions(self):
        """충돌 검사 (갈라가 특화)"""
        # 플레이어 총알 vs 적
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if self._rect_collision(
                    bullet.x, bullet.y, bullet.width, bullet.height,
                    enemy.x, enemy.y, enemy.width, enemy.height
                ):
                    self.score += 50 * (1 + enemy.type) + (self.wave * 10)

                    # 파워업 드롭 확률
                    if random.random() < 0.1:
                        power_types = ["rapid", "dual", "bomb", "shield"]
                        power_type = random.choice(power_types)
                        powerup = PowerUp(enemy.x, enemy.y, power_type)
                        self.power_ups.append(powerup)

                    if bullet in self.player.bullets:
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
                    if self.shield:
                        self.shield_health -= 10
                        if self.shield_health <= 0:
                            self.shield = False
                    else:
                        self.player.health -= 10

                    if bullet in enemy.bullets:
                        enemy.bullets.remove(bullet)

                    if self.player.health <= 0:
                        self.game_state.game_over = True

        # 적과 플레이어 충돌 (캡처)
        for enemy in self.enemies[:]:
            if self._rect_collision(
                enemy.x, enemy.y, enemy.width, enemy.height,
                self.player.x, self.player.y, self.player.width, self.player.height
            ):
                if not self.shield:
                    self.player.health -= 20
                    if self.player.health <= 0:
                        self.game_state.game_over = True

    def _rect_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        """사각형 충돌 검사"""
        return not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2)

    def draw(self):
        """화면 그리기 (갈라가 특화)"""
        self.screen.fill(self.theme.bg_color)

        # 포메이션 표시
        for enemy in self.enemies:
            enemy_color = Color.RED if enemy.type == 1 else Color.YELLOW
            pygame.draw.rect(self.screen, enemy_color, (enemy.x, enemy.y, enemy.width, enemy.height))

            # 다이브 모드 표시
            if isinstance(enemy, GalagaEnemy) and enemy.is_diving:
                pygame.draw.rect(self.screen, Color.WHITE, (enemy.x, enemy.y, enemy.width, enemy.height), 2)

        # 플레이어
        pygame.draw.rect(self.screen, Color.GREEN, (self.player.x, self.player.y, self.player.width, self.player.height))

        # 방어막 표시
        if self.shield:
            pygame.draw.circle(self.screen, Color.CYAN,
                              (int(self.player.x + self.player.width // 2),
                               int(self.player.y + self.player.height // 2)), 35, 2)

        # 총알 표시
        for bullet in self.player.bullets:
            pygame.draw.rect(self.screen, Color.GREEN, (bullet.x, bullet.y, bullet.width, bullet.height))

        for enemy in self.enemies:
            for bullet in enemy.bullets:
                pygame.draw.rect(self.screen, Color.YELLOW, (bullet.x, bullet.y, 3, 10))

        # 파워업 표시
        for powerup in self.power_ups:
            powerup.draw(self.screen, {})

        # UI
        score_text = self.font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (10, 10))

        stage_text = self.small_font.render(f"Stage: {self.stage} | Wave: {self.wave}", True, self.theme.text_color)
        self.screen.blit(stage_text, (10, 50))

        health_text = self.small_font.render(f"Health: {self.player.health}", True, self.theme.text_color)
        self.screen.blit(health_text, (10, 80))

        # 파워업 상태
        status_texts = []
        if self.dual_fire:
            status_texts.append(f"Dual Fire: {self.dual_timer//60}s")
        if self.rapid_fire:
            status_texts.append(f"Rapid Fire: {self.rapid_timer//60}s")
        if self.shield:
            status_texts.append(f"Shield: {self.shield_health}%")

        for i, status in enumerate(status_texts):
            status_text = self.small_font.render(status, True, Color.CYAN)
            self.screen.blit(status_text, (SCREEN_WIDTH - 200, 10 + i * 25))

        # Hawk 공격 표시
        if self.hawk_available:
            hawk_text = self.small_font.render("HAWK READY (SPACE)", True, Color.YELLOW)
            self.screen.blit(hawk_text, (SCREEN_WIDTH // 2 - 80, 10))
        elif self.hawk_cooldown > 0:
            hawk_text = self.small_font.render(f"Hawk: {self.hawk_cooldown//60}s", True, Color.RED)
            self.screen.blit(hawk_text, (SCREEN_WIDTH // 2 - 60, 10))

        # 일시정지
        if self.paused:
            pause_text = self.font.render("PAUSED", True, Color.RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # 게임 오버
        if self.game_state.game_over:
            over_text = self.font.render("GAME OVER", True, Color.RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))

            final_score_text = self.small_font.render(f"Final Score: {self.score}", True, Color.YELLOW)
            self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()

if __name__ == "__main__":
    game = GalagaGame()
    game.run()
