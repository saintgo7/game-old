#!/usr/bin/env python3
"""
🎮 게임 002 - SNAKE (뱀)
뱀이 움직이며 음식을 먹고 자신의 몸에 부딪히지 않게 조절하는 게임입니다.
"""

import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 게임 설정
GRID_SIZE = 20
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
FPS = 10

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 방향
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """뱀 클래스"""
    def __init__(self):
        self.body = [(SCREEN_WIDTH // (2 * GRID_SIZE), SCREEN_HEIGHT // (2 * GRID_SIZE))]
        self.direction = RIGHT
        self.next_direction = RIGHT

    def move(self):
        """뱀 이동"""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

    def grow(self):
        """뱀 길이 증가 (음식 섭취)"""
        pass  # move() 호출 시 자동으로 길어짐

    def check_collision(self):
        """자기 몸과의 충돌 확인"""
        head = self.body[0]
        return head in self.body[1:]

    def check_bounds(self):
        """경계 확인"""
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= SCREEN_WIDTH // GRID_SIZE or
                head_y < 0 or head_y >= SCREEN_HEIGHT // GRID_SIZE)

    def draw(self, screen):
        """뱀 그리기"""
        for i, (x, y) in enumerate(self.body):
            color = GREEN if i == 0 else (0, 200, 0)  # 머리는 더 밝은 녹색
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)


class Food:
    """음식 클래스"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
        self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)

    def respawn(self, snake_body):
        """새로운 위치에 음식 생성"""
        while (self.x, self.y) in snake_body:
            self.x = random.randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
            self.y = random.randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)

    def draw(self, screen):
        """음식 그리기"""
        rect = pygame.Rect(self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)


class SnakeGame:
    """Snake 게임"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 SNAKE - 게임 002")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        self.snake = Snake()
        self.food = Food()

        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                # 뱀 방향 제어
                elif event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.next_direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.next_direction = RIGHT

    def update(self):
        """게임 업데이트"""
        if self.game_over:
            return

        # 뱀 이동
        self.snake.move()

        # 음식 먹기
        if self.snake.body[0] == (self.food.x, self.food.y):
            self.score += 10
            # 새 음식 생성하기 전에 뱀 길이 증가
            self.snake.body.append(self.snake.body[-1])
            self.food.respawn(self.snake.body)
            # 게임 속도 증가
            if self.score % 50 == 0:
                global FPS
                FPS += 1

        # 충돌 확인
        if self.snake.check_collision() or self.snake.check_bounds():
            self.game_over = True

    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)

        # 뱀과 음식 그리기
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # 점수 표시
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # 길이 표시
        length_text = self.font.render(f"Length: {len(self.snake.body)}", True, WHITE)
        self.screen.blit(length_text, (SCREEN_WIDTH - 200, 10))

        # 게임 오버
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            score_final = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to play again", True, YELLOW)

            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(score_final, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80))

        pygame.display.flip()

    def reset_game(self):
        """게임 초기화"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        global FPS
        FPS = 10

    def run(self):
        """게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
