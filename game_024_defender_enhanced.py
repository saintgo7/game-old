#!/usr/bin/env python3
"""
🔫 Defender (게임 024) - 상세 구현
Defender는 클래식 슈팅게임으로, 플레이어가 우주선을 조종하여
적 함선을 격추하고 파도별로 증가하는 난이도를 극복해야 함
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from shooting_game_template import ShootingGame, GameDifficulty, Player, Enemy, Bullet, EnemyBullet

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class DefenderGame(ShootingGame):
    """Defender 게임 - 슈팅 템플릿 확장"""

    def __init__(self):
        super().__init__("Defender", difficulty=GameDifficulty.NORMAL)

        # Defender 특화 설정
        self.player.max_speed = 8
        self.player.fire_rate = 8
        self.wave_enemy_count = 3  # 초기 적 수
        self.shield_power = 100
        self.max_shield = 100

    def _spawn_enemies(self):
        """Defender 특화: 더 전략적인 적 배치"""
        self.enemies = []
        wave_difficulty = 1 + (self.wave * 0.5)

        for i in range(int(self.wave_enemy_count * wave_difficulty)):
            if random.random() < 0.7:
                # 상단에서 나타나는 적
                x = random.randint(0, SCREEN_WIDTH - 25)
                y = random.randint(20, 150)
            else:
                # 측면에서 나타나는 적
                x = random.choice([0, SCREEN_WIDTH - 25])
                y = random.randint(150, SCREEN_HEIGHT - 50)

            enemy_type = 1 + (self.wave % 3)
            enemy = Enemy(x, y, enemy_type)
            enemy.speed = 2 + (self.wave * 0.3)
            self.enemies.append(enemy)

    def update(self):
        """Defender 특화 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        # 기본 업데이트
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()

        # 적 업데이트
        for enemy in self.enemies[:]:
            enemy.update()

        # 충돌 검사
        self._check_collisions()

        # 방어막 감소
        if self.shield_power > 0:
            self.shield_power = max(0, self.shield_power - 0.1)

        # 웨이브 진행
        if len(self.enemies) == 0:
            self.wave += 1
            self.level += 1
            self.wave_enemy_count = 3 + self.wave
            self._spawn_enemies()
            # 방어막 회복
            self.shield_power = self.max_shield

    def _check_collisions(self):
        """Defender 특화: 방어막 시스템 추가"""
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
                    if self.shield_power > 0:
                        self.shield_power -= 10
                    else:
                        self.player.health -= 10
                    enemy.bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.game_state.game_over = True

    def draw(self):
        """Defender 특화: 방어막 표시"""
        super().draw()

        # 방어막 표시
        if self.shield_power > 0:
            shield_ratio = self.shield_power / self.max_shield
            shield_width = 200 * shield_ratio
            pygame.draw.rect(self.screen, (0, 150, 255), (10, 110, shield_width, 20))
            pygame.draw.rect(self.screen, (100, 200, 255), (10, 110, 200, 20), 2)

            shield_text = self.small_font.render(f"Shield: {int(self.shield_power)}", True, (100, 200, 255))
            self.screen.blit(shield_text, (10, 135))

if __name__ == "__main__":
    game = DefenderGame()
    game.run()
