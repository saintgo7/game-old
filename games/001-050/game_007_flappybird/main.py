#!/usr/bin/env python3
"""🎮 게임 007 - FLAPPY BIRD (플래피 버드)"""
import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
FPS = 60
WHITE, BLACK, YELLOW, GREEN = (255,255,255), (0,0,0), (255,255,0), (0,255,0)

class Bird:
    def __init__(self):
        self.rect = pygame.Rect(50, SCREEN_HEIGHT // 2, 40, 30)
        self.vel = 0
        self.gravity = 0.5

    def update(self):
        self.vel += self.gravity
        self.rect.y += self.vel

    def jump(self):
        self.vel = -10

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)

class Pipe:
    def __init__(self, x):
        self.gap = random.randint(100, 300)
        self.x = x
        self.width = 60
        self.speed = 4

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap))
        pygame.draw.rect(screen, GREEN, (self.x, self.gap + 150, self.width, SCREEN_HEIGHT - self.gap - 150))

    def off_screen(self):
        return self.x + self.width < 0

class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 FLAPPY BIRD - 게임 007")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.running = True
        self.game_over = False
        self.pipe_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.bird.jump()

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        if self.bird.rect.top < 0 or self.bird.rect.bottom > SCREEN_HEIGHT:
            self.game_over = True

        self.pipe_timer += 1
        if self.pipe_timer > 100:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.pipe_timer = 0

        for pipe in self.pipes[:]:
            pipe.update()
            if pipe.off_screen():
                self.pipes.remove(pipe)
                self.score += 1

            if (self.bird.rect.left < pipe.x + pipe.width and
                self.bird.rect.right > pipe.x and
                (self.bird.rect.top < pipe.gap or self.bird.rect.bottom > pipe.gap + 150)):
                self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("GAME OVER", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    FlappyBirdGame().run()
