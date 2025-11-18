#!/usr/bin/env python3
"""
🔥 Ikaruga (게임 141) - 탄막 슈팅 게임
회피 중심의 탄막 슈팅으로 흑백 색상 전환이 핵심 메커니즘
"""

import pygame, random, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from shooting_game_template import ShootingGame, GameDifficulty, Player, Enemy
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class IkarugaBullet:
    """이카루가 총알 - 색상 속성 추가"""
    def __init__(self, x, y, color="white"):
        self.x, self.y = x, y
        self.width, self.height = 3, 10
        self.speed = 8
        self.color = color  # "white" or "black"

    def update(self):
        self.y -= self.speed
        
    def draw(self, surface):
        col = Color.WHITE if self.color == "white" else Color.BLACK
        pygame.draw.rect(surface, col, (self.x, self.y, self.width, self.height))

class IkarugaEnemy:
    """이카루가 적"""
    def __init__(self, x, y, bullet_color="white"):
        self.x, self.y = x, y
        self.width, self.height = 25, 25
        self.health = 1
        self.speed = 2
        self.bullet_color = bullet_color
        self.fire_rate = 30
        self.bullets = []
        self.pattern_time = 0

    def update(self):
        self.pattern_time += 1
        # 파도 이동
        self.x += math.sin(self.pattern_time * 0.05) * 1.5
        self.bullets = [b for b in self.bullets if b.y > -20]
        for b in self.bullets:
            b.update()

    def draw(self, surface):
        col = Color.YELLOW if self.bullet_color == "white" else Color.CYAN
        pygame.draw.rect(surface, col, (self.x, self.y, self.width, self.height))

class IkarugaGame(ShootingGame):
    """Ikaruga 게임"""
    def __init__(self):
        super().__init__("Ikaruga", difficulty=GameDifficulty.NORMAL)
        self.player_color = "white"  # 플레이어 색상
        self.color_change_cooldown = 0
        self.enemies = []
        self.wave = 0
        self._spawn_enemies()

    def _spawn_enemies(self):
        """적 생성"""
        self.enemies = []
        for _ in range(3 + self.wave):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(20, 150)
            color = random.choice(["white", "black"])
            enemy = IkarugaEnemy(x, y, color)
            self.enemies.append(enemy)

    def update(self):
        if self.paused or self.game_state.game_over:
            return

        keys = pygame.key.get_pressed()
        
        # 움직임
        if keys[pygame.K_LEFT]:
            self.player.x = max(0, self.player.x - 5)
        if keys[pygame.K_RIGHT]:
            self.player.x = min(SCREEN_WIDTH - self.player.width, self.player.x + 5)
        if keys[pygame.K_UP]:
            self.player.y = max(0, self.player.y - 5)
        if keys[pygame.K_DOWN]:
            self.player.y = min(SCREEN_HEIGHT - self.player.height, self.player.y + 5)

        # 색상 전환 (X키)
        if keys[pygame.K_x] and self.color_change_cooldown <= 0:
            self.player_color = "black" if self.player_color == "white" else "white"
            self.color_change_cooldown = 20

        # 발사
        if keys[pygame.K_SPACE] and random.random() < 0.3:
            bullet = IkarugaBullet(self.player.x + 10, self.player.y, self.player_color)
            self.player.bullets.append(bullet)

        self.color_change_cooldown = max(0, self.color_change_cooldown - 1)
        self.player.bullets = [b for b in self.player.bullets if b.y > -20]
        for b in self.player.bullets:
            b.update()

        # 적 업데이트
        for enemy in self.enemies[:]:
            enemy.update()
            if random.random() < 0.02:
                bullet = IkarugaBullet(enemy.x, enemy.y + enemy.height, enemy.bullet_color)
                bullet.speed = -4
                enemy.bullets.append(bullet)

        # 충돌 검사
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and 
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    # 색상 매칭 시에만 데미지
                    if bullet.color == enemy.bullet_color:
                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        self.score += 100
                        break

        # 적 총알 vs 플레이어
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if (bullet.x < self.player.x + self.player.width and 
                    bullet.x + 3 > self.player.x and
                    bullet.y < self.player.y + self.player.height and
                    bullet.y + 10 > self.player.y):
                    # 같은 색상이면 상쇄, 다르면 피해
                    if bullet.color != self.player_color:
                        self.player.health -= 10
                    enemy.bullets.remove(bullet)
                    if self.player.health <= 0:
                        self.game_state.game_over = True

        # 웨이브 진행
        if len(self.enemies) == 0:
            self.wave += 1
            self.score += 500
            self._spawn_enemies()

    def draw(self):
        """그리기"""
        self.screen.fill(self.theme.bg_color)

        # 플레이어
        col = Color.GREEN if self.player_color == "white" else Color.RED
        pygame.draw.rect(self.screen, col, (self.player.x, self.player.y, self.player.width, self.player.height))
        pygame.draw.rect(self.screen, Color.WHITE, (self.player.x, self.player.y, self.player.width, self.player.height), 2)

        # 적
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # 총알
        for bullet in self.player.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            for bullet in enemy.bullets:
                bullet.draw(self.screen)

        # UI
        score_text = self.font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (10, 10))
        
        wave_text = self.small_font.render(f"Wave: {self.wave} | Health: {self.player.health}", True, Color.GREEN)
        self.screen.blit(wave_text, (10, 50))
        
        color_text = self.small_font.render(f"Color: {self.player_color.upper()} (X)", True, col)
        self.screen.blit(color_text, (SCREEN_WIDTH - 200, 10))

        if self.game_state.game_over:
            over = self.font.render("GAME OVER", True, Color.RED)
            self.screen.blit(over, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    game = IkarugaGame()
    game.run()
