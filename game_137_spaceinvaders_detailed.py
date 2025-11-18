#!/usr/bin/env python3
"""
Space Invaders - 상세 구현
클래식 슈팅 게임: 플레이어는 화면 하단에서 적들을 격추
"""
import pygame
import random
import math
from shooting_game_template import ShootingGame, Player, Enemy, Bullet
from graphics_themes import Color, Themes, ParticleSystem

class InvaderEnemy(Enemy):
    """우주 침략자"""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 15
        self.color = Color.GREEN
        self.speed = 1
        self.direction = 1  # 1 = 우측, -1 = 좌측
        self.wave_offset = 0
        self.wave_phase = 0

    def update(self, dt):
        """침략자 업데이트"""
        self.wave_phase += 0.05
        self.y += self.speed * (dt / 1000.0)
        self.x += self.direction * 0.5 * math.cos(self.wave_phase)

        # 화면 가장자리에서 방향 변경
        if self.x < 0 or self.x > 800:
            self.direction *= -1

    def draw(self, surface):
        """침략자 그리기 (간단한 삼각형)"""
        pygame.draw.polygon(surface, self.color, [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ])

    def get_rect(self):
        """충돌 범위"""
        return pygame.Rect(self.x - self.size, self.y - self.size,
                          self.size * 2, self.size * 2)


class SpaceInvadersGame(ShootingGame):
    """Space Invaders 상세 구현"""

    def __init__(self):
        super().__init__()
        self.window_width = 800
        self.window_height = 600
        self.game_name = "Space Invaders"

        # 게임 상태
        self.level = 1
        self.wave = 0
        self.enemies_killed = 0
        self.enemies_per_wave = 8

        # 파티클 시스템
        self.particles = ParticleSystem()

        # 테마 설정
        self.theme = Themes.RETRO

        # 플레이어 설정
        self.player = Player(self.window_width // 2, self.window_height - 50)
        self.player.speed = 300

        # 게임 루프
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_over_time = 0

        self._spawn_wave()

    def _spawn_wave(self):
        """적 웨이브 생성"""
        self.wave += 1
        self.enemies = []

        # 웨이브가 올라갈수록 더 많은 적 생성
        num_enemies = self.enemies_per_wave + (self.wave // 2)

        for i in range(num_enemies):
            x = (i % 4) * 150 + 100
            y = (i // 4) * 60 + 30
            enemy = InvaderEnemy(x, y)
            enemy.speed = 0.5 + (self.level * 0.1)
            self.enemies.append(enemy)

    def _check_collisions(self):
        """충돌 확인"""
        # 적과 플레이어 총알 충돌
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.enemies_killed += 1

                    # 폭발 이펙트
                    self.particles.emit_explosion(enemy.x, enemy.y, Color.YELLOW, 10)
                    break

        # 적과 플레이어 충돌
        player_rect = self.player.get_rect()
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.game_over = True
                self.game_over_time = pygame.time.get_ticks()
                self.particles.emit_explosion(self.player.x, self.player.y, Color.RED, 20)

        # 적이 화면 하단에 도달
        for enemy in self.enemies[:]:
            if enemy.y > self.window_height:
                self.game_over = True
                self.game_over_time = pygame.time.get_ticks()

        # 모든 적을 격추했을 때 다음 웨이브
        if len(self.enemies) == 0 and self.wave > 0:
            self.level += 1
            self._spawn_wave()

    def _handle_input(self):
        """입력 처리"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left(16)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right(16, self.window_width)
        if keys[pygame.K_SPACE]:
            self.player.shoot()

    def _update(self, dt):
        """게임 업데이트"""
        if self.game_over:
            return

        self._handle_input()

        # 플레이어 업데이트
        self.player.update(dt)

        # 적 업데이트
        for enemy in self.enemies:
            enemy.update(dt)

        # 총알 업데이트
        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.y < 0:
                self.bullets.remove(bullet)

        # 충돌 확인
        self._check_collisions()

        # 파티클 업데이트
        self.particles.update(dt)

    def _draw(self, surface):
        """화면 그리기"""
        surface.fill(self.theme.bg_color)

        # 플레이어 그리기
        pygame.draw.circle(surface, self.theme.primary_color,
                          (int(self.player.x), int(self.player.y)), 10)

        # 적 그리기
        for enemy in self.enemies:
            enemy.draw(surface)

        # 총알 그리기
        for bullet in self.bullets:
            bullet.draw(surface)

        # 파티클 그리기
        self.particles.draw(surface)

        # 점수 및 레벨 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.theme.primary_color)
        level_text = font.render(f"Level: {self.level} Wave: {self.wave}", True, self.theme.primary_color)
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 50))

        # 게임 오버 화면
        if self.game_over:
            font_large = pygame.font.Font(None, 80)
            go_text = font_large.render("GAME OVER", True, Color.RED)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            surface.blit(go_text, go_rect)

    def run(self):
        """게임 실행"""
        pygame.init()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.game_name)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            dt = self.clock.tick(60)  # 60 FPS
            self._update(dt)
            self._draw(self.display)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = SpaceInvadersGame()
    game.run()
