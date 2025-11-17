#!/usr/bin/env python3
"""🎮 게임 004 - BREAKOUT (벽돌깨기)"""
import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
WHITE, BLACK, COLORS = (255, 255, 255), (0, 0, 0), [(255,0,0), (0,255,0), (0,0,255), (255,255,0)]

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 30, 100, 15)
        self.speed = 7

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, 10)
        self.speed_x, self.speed_y = random.choice([-4, 4]), -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        return self.rect.bottom >= SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 60, 20)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class BreakoutGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 BREAKOUT - 게임 004")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(x, y, COLORS[(y // 25) % 4])
                       for y in range(50, 200, 25)
                       for x in range(20, SCREEN_WIDTH - 20, 70)]
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
        self.paddle.move(keys)

        if self.ball.update():
            self.game_over = True

        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.speed_y = -self.ball.speed_y

        for brick in self.bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.speed_y = -self.ball.speed_y
                self.bricks.remove(brick)
                self.score += 10

        if not self.bricks:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("GAME OVER" if self.ball.rect.bottom >= SCREEN_HEIGHT else "YOU WIN!", True, WHITE)
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
    BreakoutGame().run()
