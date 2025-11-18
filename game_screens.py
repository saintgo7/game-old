#!/usr/bin/env python3
"""
게임 인트로/아웃트로 화면 시스템
- 게임 시작 화면
- 게임 오버 화면
- 일시정지 화면
- 레벨 시작 화면
"""
import pygame
from enum import Enum
from graphics_themes import Color, Theme, Themes, Animation, FadeAnimation, ParticleSystem


class ScreenType(Enum):
    """화면 타입"""
    INTRO = 1
    LEVEL_START = 2
    PAUSE = 3
    GAME_OVER = 4
    VICTORY = 5


class GameScreen:
    """게임 화면 기본 클래스"""

    def __init__(self, width=800, height=600, theme=None):
        self.width = width
        self.height = height
        self.theme = theme or Themes.CLASSIC
        self.surface = None
        self.done = False
        self.particles = ParticleSystem()

    def setup(self, surface):
        """화면 설정"""
        self.surface = surface

    def handle_event(self, event):
        """이벤트 처리"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.done = True

    def update(self, dt):
        """화면 업데이트"""
        self.particles.update(dt)

    def draw(self):
        """화면 그리기"""
        self.surface.fill(self.theme.bg_color)
        self.particles.draw(self.surface)

    def is_done(self):
        """화면이 끝났는지 확인"""
        return self.done


class IntroScreen(GameScreen):
    """게임 인트로 화면"""

    def __init__(self, game_name, width=800, height=600, theme=None):
        super().__init__(width, height, theme)
        self.game_name = game_name
        self.fade = FadeAnimation(2000, start_alpha=0, end_alpha=255)
        self.elapsed = 0
        self.total_duration = 4000  # 4초

    def update(self, dt):
        """인트로 업데이트"""
        super().update(dt)
        self.fade.update(dt)
        self.elapsed += dt

        # 4초 후 자동으로 진행
        if self.elapsed >= self.total_duration:
            self.done = True

        # 스파클 효과
        if self.elapsed % 100 < 16:  # 매 100ms마다 파티클 방출
            self.particles.emit_sparkle(
                self.width // 2 + pygame.math.Vector2(1, 0).x * 50,
                self.height // 2,
                color=self.theme.primary_color,
                count=3
            )

    def draw(self):
        """인트로 화면 그리기"""
        super().draw()

        font_large = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 40)

        # 제목
        title_text = font_large.render(self.game_name, True, self.theme.primary_color)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.surface.blit(title_text, title_rect)

        # 준비 메시지 (깜빡임)
        alpha_factor = abs((self.elapsed % 1000) / 500.0 - 1.0)  # 0~1~0
        if alpha_factor > 0.5:
            ready_text = font_small.render("PRESS SPACE TO START", True, self.theme.secondary_color)
            ready_rect = ready_text.get_rect(center=(self.width // 2, self.height // 2 + 100))
            self.surface.blit(ready_text, ready_rect)


class LevelStartScreen(GameScreen):
    """레벨 시작 화면"""

    def __init__(self, level_num, width=800, height=600, theme=None):
        super().__init__(width, height, theme)
        self.level_num = level_num
        self.elapsed = 0
        self.total_duration = 2000  # 2초

    def update(self, dt):
        """레벨 시작 화면 업데이트"""
        super().update(dt)
        self.elapsed += dt

        # 2초 후 자동으로 진행
        if self.elapsed >= self.total_duration:
            self.done = True

    def draw(self):
        """레벨 시작 화면 그리기"""
        super().draw()

        font = pygame.font.Font(None, 100)
        text = font.render(f"LEVEL {self.level_num}", True, self.theme.primary_color)
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.surface.blit(text, text_rect)


class PauseScreen(GameScreen):
    """일시정지 화면"""

    def __init__(self, width=800, height=600, theme=None):
        super().__init__(width, height, theme)
        self.menu_index = 0
        self.menu_items = ["RESUME", "QUIT"]

    def handle_event(self, event):
        """일시정지 화면 이벤트 처리"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.done = True
            elif event.key == pygame.K_ESCAPE:
                self.menu_index = 0
                self.done = True

    def draw(self):
        """일시정지 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(Color.BLACK)
        self.surface.blit(overlay, (0, 0))

        font_title = pygame.font.Font(None, 80)
        font_menu = pygame.font.Font(None, 50)

        # 제목
        title_text = font_title.render("PAUSE", True, self.theme.primary_color)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 150))
        self.surface.blit(title_text, title_rect)

        # 메뉴 항목
        for i, item in enumerate(self.menu_items):
            y_pos = self.height // 2 + i * 80

            if i == self.menu_index:
                # 선택된 항목
                color = self.theme.secondary_color
                prefix = "> "
            else:
                color = self.theme.primary_color
                prefix = "  "

            text = font_menu.render(prefix + item, True, color)
            text_rect = text.get_rect(center=(self.width // 2, y_pos))
            self.surface.blit(text, text_rect)


class GameOverScreen(GameScreen):
    """게임 오버 화면"""

    def __init__(self, score=0, level=1, width=800, height=600, theme=None, is_victory=False):
        super().__init__(width, height, theme)
        self.score = score
        self.level = level
        self.is_victory = is_victory
        self.particles = ParticleSystem()
        self.elapsed = 0

        # 승리/패배에 따라 파티클 방출
        if is_victory:
            for _ in range(5):
                self.particles.emit_explosion(
                    self.width // 2,
                    self.height // 2,
                    color=Color.YELLOW,
                    count=15
                )

    def update(self, dt):
        """게임 오버 화면 업데이트"""
        super().update(dt)
        self.elapsed += dt

    def draw(self):
        """게임 오버 화면 그리기"""
        super().draw()

        font_title = pygame.font.Font(None, 80)
        font_text = pygame.font.Font(None, 50)
        font_small = pygame.font.Font(None, 35)

        # 제목
        if self.is_victory:
            title_text = font_title.render("VICTORY!", True, Color.YELLOW)
        else:
            title_text = font_title.render("GAME OVER", True, Color.RED)

        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 2 - 150))
        self.surface.blit(title_text, title_rect)

        # 점수 및 레벨 정보
        score_text = font_text.render(f"Score: {self.score:,}", True, self.theme.primary_color)
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        self.surface.blit(score_text, score_rect)

        level_text = font_text.render(f"Level: {self.level}", True, self.theme.primary_color)
        level_rect = level_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        self.surface.blit(level_text, level_rect)

        # 지속 메시지
        continue_text = font_small.render("Press SPACE to continue", True, self.theme.secondary_color)
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 150))
        self.surface.blit(continue_text, continue_rect)


class ScreenManager:
    """화면 관리자"""

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.current_screen: GameScreen = None
        self.screen_history = []

    def show_screen(self, screen: GameScreen):
        """화면 표시"""
        self.current_screen = screen

    def show_intro(self, game_name, theme=None):
        """인트로 화면 표시"""
        screen = IntroScreen(game_name, self.width, self.height, theme)
        self.show_screen(screen)

    def show_level_start(self, level_num, theme=None):
        """레벨 시작 화면 표시"""
        screen = LevelStartScreen(level_num, self.width, self.height, theme)
        self.show_screen(screen)

    def show_pause(self, theme=None):
        """일시정지 화면 표시"""
        screen = PauseScreen(self.width, self.height, theme)
        self.show_screen(screen)

    def show_game_over(self, score=0, level=1, theme=None, is_victory=False):
        """게임 오버 화면 표시"""
        screen = GameOverScreen(score, level, self.width, self.height, theme, is_victory)
        self.show_screen(screen)

    def update(self, dt, surface):
        """화면 업데이트"""
        if self.current_screen:
            self.current_screen.setup(surface)
            self.current_screen.update(dt)
            self.current_screen.draw()

    def handle_event(self, event):
        """이벤트 처리"""
        if self.current_screen:
            self.current_screen.handle_event(event)

    def is_done(self):
        """현재 화면이 끝났는지 확인"""
        if self.current_screen:
            return self.current_screen.is_done()
        return False

    def clear_current(self):
        """현재 화면 제거"""
        self.current_screen = None
