#!/usr/bin/env python3
"""
🎮 게임 001 - PONG (탁구)
클래식 탁구 게임. 공이 화면을 움직이고 양쪽 끝의 패들로 공을 반사시키는 게임입니다.
"""

import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# 클래스 정의
class Paddle:
    """패들 (탁구 라켓)"""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 100)
        self.speed = 6

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    """공"""
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 15, 15)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 상하 경계 충돌
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def reset(self):
        """공 리셋"""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class PongGame:
    """Pong 게임 메인 클래스"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 PONG - 게임 001")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # 게임 요소
        self.left_paddle = Paddle(20, SCREEN_HEIGHT // 2 - 50)
        self.right_paddle = Paddle(SCREEN_WIDTH - 35, SCREEN_HEIGHT // 2 - 50)
        self.ball = Ball()

        # 점수
        self.left_score = 0
        self.right_score = 0

        # 게임 상태
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

    def handle_input(self):
        """입력 처리"""
        keys = pygame.key.get_pressed()

        # 왼쪽 패들 조작 (W, S)
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        # 오른쪽 패들 조작 (UP, DOWN)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

    def update(self):
        """게임 업데이트"""
        if self.game_over:
            return

        # 공 업데이트
        self.ball.update()

        # 패들과 공 충돌 감지
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.speed_x = abs(self.ball.speed_x)
            self.ball.speed_y += random.choice([-1, 1])

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.speed_x = -abs(self.ball.speed_x)
            self.ball.speed_y += random.choice([-1, 1])

        # 좌우 경계 확인 (게임 끝)
        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()
            if self.right_score >= 11:
                self.game_over = True

        if self.ball.rect.right >= SCREEN_WIDTH:
            self.left_score += 1
            self.ball.reset()
            if self.left_score >= 11:
                self.game_over = True

    def draw(self):
        """화면 렌더링"""
        self.screen.fill(BLACK)

        # 중앙 선 그리기
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.screen, GRAY, (SCREEN_WIDTH // 2, y),
                           (SCREEN_WIDTH // 2, y + 10), 2)

        # 게임 요소 그리기
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # 점수 표시
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (SCREEN_WIDTH // 4, 50))
        self.screen.blit(right_text, (SCREEN_WIDTH * 3 // 4 - 50, 50))

        # 조작 방법
        control_text = self.small_font.render("W/S: Left, UP/DOWN: Right", True, GRAY)
        self.screen.blit(control_text, (20, SCREEN_HEIGHT - 40))

        # 게임 오버 화면
        if self.game_over:
            winner = "LEFT" if self.left_score > self.right_score else "RIGHT"
            game_over_text = self.font.render(f"{winner} WINS!", True, WHITE)
            reset_text = self.small_font.render("Press SPACE to play again", True, GRAY)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(reset_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

    def reset_game(self):
        """게임 초기화"""
        self.left_score = 0
        self.right_score = 0
        self.ball.reset()
        self.game_over = False

    def run(self):
        """게임 루프"""
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PongGame()
    game.run()
