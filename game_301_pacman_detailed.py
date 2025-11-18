#!/usr/bin/env python3
"""
Pac-Man - 상세 구현
클래식 액션 게임: 미로를 돌아다니며 점을 먹고 귀신을 피함
"""
import pygame
import random
from graphics_themes import Color, Themes

class Ghost:
    """귀신 AI"""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 15
        self.speed = 2
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move_counter = 0
        self.move_interval = 30

    def update(self, board, pacman_x, pacman_y):
        """귀신 업데이트 (간단한 AI)"""
        self.move_counter += 1

        if self.move_counter >= self.move_interval:
            self.move_counter = 0

            # 팩맨 방향으로 이동 시도
            if random.random() < 0.7:
                # 70% 확률로 팩맨 방향으로 이동
                dx = 1 if pacman_x > self.x else -1
                dy = 1 if pacman_y > self.y else -1

                if random.random() < 0.5:
                    self.direction = (dx, 0)
                else:
                    self.direction = (0, dy)

        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed

        # 경계 확인
        if 0 <= new_x < 800 and 0 <= new_y < 600:
            self.x = new_x
            self.y = new_y
        else:
            self.direction = tuple(-d for d in self.direction)

    def draw(self, surface):
        """귀신 그리기"""
        # 원형 몸체
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        # 눈
        pygame.draw.circle(surface, Color.WHITE, (int(self.x - 5), int(self.y - 3)), 3)
        pygame.draw.circle(surface, Color.WHITE, (int(self.x + 5), int(self.y - 3)), 3)

    def get_rect(self):
        """충돌 범위"""
        return pygame.Rect(self.x - self.size, self.y - self.size,
                          self.size * 2, self.size * 2)


class PacManGame:
    """Pac-Man 상세 구현"""

    def __init__(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.game_name = "Pac-Man"

        # 게임 상태
        self.pacman_x = self.window_width // 2
        self.pacman_y = self.window_height // 2
        self.pacman_speed = 3
        self.pacman_size = 12
        self.pacman_direction = (1, 0)
        self.pacman_next_direction = (1, 0)

        # 점들
        self.dots = []
        self.power_ups = []
        self._create_dots()

        # 귀신들
        self.ghosts = [
            Ghost(100, 100, Color.RED),
            Ghost(700, 100, Color.MAGENTA),
            Ghost(100, 500, Color.CYAN),
            Ghost(700, 500, Color.YELLOW)
        ]

        # 게임 상태
        self.score = 0
        self.level = 1
        self.game_over = False
        self.power_up_mode = False
        self.power_up_time = 0

        # 테마
        self.theme = Themes.CLASSIC

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.game_name)

        self.running = True

    def _create_dots(self):
        """점 생성"""
        self.dots = []
        for x in range(50, self.window_width, 40):
            for y in range(50, self.window_height, 40):
                if not (abs(x - self.pacman_x) < 50 and abs(y - self.pacman_y) < 50):
                    self.dots.append((x, y))

        # 파워업 생성
        self.power_ups = [
            (100, 100),
            (self.window_width - 100, 100),
            (100, self.window_height - 100),
            (self.window_width - 100, self.window_height - 100)
        ]

    def _handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.pacman_next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.pacman_next_direction = (1, 0)
                elif event.key == pygame.K_UP:
                    self.pacman_next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.pacman_next_direction = (0, 1)

    def _update(self, dt):
        """게임 업데이트"""
        if self.game_over:
            return

        # 팩맨 이동
        self.pacman_direction = self.pacman_next_direction
        new_x = self.pacman_x + self.pacman_direction[0] * self.pacman_speed
        new_y = self.pacman_y + self.pacman_direction[1] * self.pacman_speed

        # 경계 래핑
        if new_x < 0:
            new_x = self.window_width
        elif new_x > self.window_width:
            new_x = 0

        if new_y < 0:
            new_y = self.window_height
        elif new_y > self.window_height:
            new_y = 0

        self.pacman_x = new_x
        self.pacman_y = new_y

        # 점 먹기
        pacman_rect = pygame.Rect(self.pacman_x - self.pacman_size,
                                 self.pacman_y - self.pacman_size,
                                 self.pacman_size * 2, self.pacman_size * 2)

        for dot in self.dots[:]:
            dot_rect = pygame.Rect(dot[0] - 3, dot[1] - 3, 6, 6)
            if pacman_rect.colliderect(dot_rect):
                self.dots.remove(dot)
                self.score += 10

        # 파워업 먹기
        for power_up in self.power_ups[:]:
            pu_rect = pygame.Rect(power_up[0] - 5, power_up[1] - 5, 10, 10)
            if pacman_rect.colliderect(pu_rect):
                self.power_ups.remove(power_up)
                self.power_up_mode = True
                self.power_up_time = 5000  # 5초

        # 귀신 업데이트
        for ghost in self.ghosts:
            ghost.update(None, self.pacman_x, self.pacman_y)

            # 팩맨과 귀신 충돌
            if pacman_rect.colliderect(ghost.get_rect()):
                if self.power_up_mode:
                    self.ghosts.remove(ghost)
                    self.score += 200
                else:
                    self.game_over = True

        # 모든 점을 먹었을 때
        if len(self.dots) == 0 and len(self.power_ups) == 0:
            self.level += 1
            self._create_dots()

        # 파워업 시간 감소
        if self.power_up_mode:
            self.power_up_time -= dt
            if self.power_up_time <= 0:
                self.power_up_mode = False

    def _draw(self, surface):
        """화면 그리기"""
        surface.fill(self.theme.bg_color)

        # 점 그리기
        for dot in self.dots:
            pygame.draw.circle(surface, Color.WHITE, dot, 3)

        # 파워업 그리기
        for power_up in self.power_ups:
            pygame.draw.circle(surface, Color.YELLOW, power_up, 5)

        # 팩맨 그리기
        pacman_color = Color.YELLOW
        pygame.draw.circle(surface, pacman_color, (int(self.pacman_x), int(self.pacman_y)), self.pacman_size)

        # 귀신 그리기
        for ghost in self.ghosts:
            if self.power_up_mode:
                ghost.color = Color.BLUE
            ghost.draw(surface)

        # 점수 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.theme.primary_color)
        level_text = font.render(f"Level: {self.level}", True, self.theme.primary_color)
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (10, 50))

        # 게임 오버
        if self.game_over:
            font_large = pygame.font.Font(None, 60)
            go_text = font_large.render("GAME OVER", True, Color.RED)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            surface.blit(go_text, go_rect)

    def run(self):
        """게임 실행"""
        while self.running:
            self._handle_input()
            dt = self.clock.tick(60)
            self._update(dt)
            self._draw(self.display)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = PacManGame()
    game.run()
