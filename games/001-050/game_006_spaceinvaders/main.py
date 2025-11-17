#!/usr/bin/env python3
"""🎮 게임 006 - SPACE INVADERS (스페이스 인베이더)"""
import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE, BLACK, GREEN = (255,255,255), (0,0,0), (0,255,0)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 50, 40)
        self.bullets = []

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 5

    def shoot(self):
        self.bullets.append(pygame.Rect(self.rect.centerx - 2, self.rect.top, 4, 10))

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, bullet)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.speed = 2

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class SpaceInvadersGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 SPACE INVADERS - 게임 006")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.player = Player()
        self.enemies = [Enemy(x, y) for y in range(50, 200, 50) for x in range(50, SCREEN_WIDTH - 50, 100)]
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        for bullet in self.player.bullets[:]:
            bullet.y -= 10
            if bullet.top < 0:
                self.player.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.rect.y += enemy.speed
            if enemy.rect.top > SCREEN_HEIGHT:
                self.game_over = True
                return

            for bullet in self.player.bullets[:]:
                if bullet.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self.player.bullets.remove(bullet)
                    self.score += 10
                    break

        if not self.enemies:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("GAME OVER" if self.enemies else "YOU WIN!", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    SpaceInvadersGame().run()
