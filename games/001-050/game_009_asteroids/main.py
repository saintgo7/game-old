#!/usr/bin/env python3
"""🎮 게임 009 - ASTEROIDS (애스터로이드)"""
import pygame
import random
import math
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE, BLACK = (255,255,255), (0,0,0)

class Player:
    def __init__(self):
        self.x, self.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.angle = 0
        self.vel_x, self.vel_y = 0, 0
        self.bullets = []

    def rotate(self, angle):
        self.angle += angle

    def accelerate(self):
        self.vel_x += math.cos(self.angle) * 0.5
        self.vel_y += math.sin(self.angle) * 0.5
        speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
        if speed > 5:
            self.vel_x = (self.vel_x / speed) * 5
            self.vel_y = (self.vel_y / speed) * 5

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x < 0: self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH: self.x = 0
        if self.y < 0: self.y = SCREEN_HEIGHT
        if self.y > SCREEN_HEIGHT: self.y = 0

    def shoot(self):
        bullet_x = self.x + math.cos(self.angle) * 20
        bullet_y = self.y + math.sin(self.angle) * 20
        bullet_vel_x = self.vel_x + math.cos(self.angle) * 7
        bullet_vel_y = self.vel_y + math.sin(self.angle) * 7
        self.bullets.append([bullet_x, bullet_y, bullet_vel_x, bullet_vel_y])

    def draw(self, screen):
        points = [(math.cos(self.angle - math.pi/2) * 15 + self.x,
                   math.sin(self.angle - math.pi/2) * 15 + self.y),
                  (math.cos(self.angle + math.pi*5/6) * 15 + self.x,
                   math.sin(self.angle + math.pi*5/6) * 15 + self.y),
                  (math.cos(self.angle - math.pi*5/6) * 15 + self.x,
                   math.sin(self.angle - math.pi*5/6) * 15 + self.y)]
        pygame.draw.polygon(screen, WHITE, points)
        for bullet in self.bullets:
            pygame.draw.circle(screen, WHITE, (int(bullet[0]), int(bullet[1])), 2)

class Asteroid:
    def __init__(self, x, y, size):
        self.x, self.y = x, y
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.size = size

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x < 0: self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH: self.x = 0
        if self.y < 0: self.y = SCREEN_HEIGHT
        if self.y > SCREEN_HEIGHT: self.y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

class AsteroidsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 ASTEROIDS - 게임 009")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.player = Player()
        self.asteroids = [Asteroid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), 15) for _ in range(5)]
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rotate(-0.1)
        if keys[pygame.K_RIGHT]:
            self.player.rotate(0.1)
        if keys[pygame.K_UP]:
            self.player.accelerate()
        if keys[pygame.K_SPACE]:
            self.player.shoot()

        self.player.update()

        for bullet in self.player.bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
                self.player.bullets.remove(bullet)

        for asteroid in self.asteroids[:]:
            asteroid.update()
            for bullet in self.player.bullets[:]:
                dist = math.sqrt((asteroid.x - bullet[0])**2 + (asteroid.y - bullet[1])**2)
                if dist < asteroid.size:
                    self.asteroids.remove(asteroid)
                    self.player.bullets.remove(bullet)
                    self.score += 10
                    break

            dist = math.sqrt((self.player.x - asteroid.x)**2 + (self.player.y - asteroid.y)**2)
            if dist < asteroid.size + 15:
                self.game_over = True

        if not self.asteroids:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.player.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("GAME OVER" if not self.asteroids else "YOU WIN!", True, WHITE)
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
    AsteroidsGame().run()
