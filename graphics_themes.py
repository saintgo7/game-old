#!/usr/bin/env python3
"""
그래픽 테마 및 디자인 시스템
"""
import pygame

class Color:
    """색상 팔레트"""
    # 기본 색상
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)

    # 원색
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    # 파스텔
    LIGHT_RED = (255, 127, 127)
    LIGHT_GREEN = (127, 255, 127)
    LIGHT_BLUE = (127, 127, 255)

    # 어두운 색
    DARK_RED = (128, 0, 0)
    DARK_GREEN = (0, 128, 0)
    DARK_BLUE = (0, 0, 128)


class Theme:
    """게임 테마"""

    def __init__(self, name, bg_color, primary_color, secondary_color, text_color):
        self.name = name
        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.text_color = text_color


# 사전 정의된 테마들
class Themes:
    """테마 모음"""

    CLASSIC = Theme(
        "classic",
        bg_color=Color.BLACK,
        primary_color=Color.WHITE,
        secondary_color=Color.YELLOW,
        text_color=Color.WHITE
    )

    DARK = Theme(
        "dark",
        bg_color=Color.DARK_GRAY,
        primary_color=Color.WHITE,
        secondary_color=Color.CYAN,
        text_color=Color.WHITE
    )

    LIGHT = Theme(
        "light",
        bg_color=Color.WHITE,
        primary_color=Color.BLACK,
        secondary_color=Color.BLUE,
        text_color=Color.BLACK
    )

    NEON = Theme(
        "neon",
        bg_color=(10, 10, 30),
        primary_color=(0, 255, 255),
        secondary_color=(255, 0, 255),
        text_color=(0, 255, 255)
    )

    RETRO = Theme(
        "retro",
        bg_color=(20, 20, 60),
        primary_color=(255, 100, 0),
        secondary_color=(0, 255, 0),
        text_color=(255, 255, 0)
    )

    FOREST = Theme(
        "forest",
        bg_color=(34, 139, 34),
        primary_color=(144, 238, 144),
        secondary_color=(255, 215, 0),
        text_color=(240, 255, 240)
    )

    OCEAN = Theme(
        "ocean",
        bg_color=(25, 25, 112),
        primary_color=(0, 191, 255),
        secondary_color=(0, 255, 127),
        text_color=(240, 255, 255)
    )


class GraphicsHelper:
    """그래픽 헬퍼 함수들"""

    @staticmethod
    def draw_rounded_rect(surface, color, rect, radius=5):
        """둥근 모서리 사각형 그리기"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    @staticmethod
    def draw_gradient_rect(surface, color1, color2, rect, vertical=True):
        """그라디언트 사각형 그리기"""
        if vertical:
            for y in range(rect.height):
                ratio = y / max(1, rect.height)
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b),
                               (rect.left, rect.top + y),
                               (rect.right, rect.top + y))
        else:
            for x in range(rect.width):
                ratio = x / max(1, rect.width)
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b),
                               (rect.left + x, rect.top),
                               (rect.left + x, rect.bottom))

    @staticmethod
    def draw_text(surface, text, font, color, rect, align="center"):
        """텍스트 그리기"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align == "center":
            text_rect.center = rect.center
        elif align == "left":
            text_rect.midleft = rect.midleft
        elif align == "right":
            text_rect.midright = rect.midright

        surface.blit(text_surface, text_rect)
        return text_rect

    @staticmethod
    def draw_button(surface, text, font, color, bg_color, rect):
        """버튼 그리기"""
        pygame.draw.rect(surface, bg_color, rect)
        pygame.draw.rect(surface, color, rect, 2)
        GraphicsHelper.draw_text(surface, text, font, color, rect)

    @staticmethod
    def draw_health_bar(surface, current, max_val, rect, color):
        """체력바 그리기"""
        # 배경
        pygame.draw.rect(surface, Color.DARK_GRAY, rect)
        # 체력
        if max_val > 0:
            health_width = int(rect.width * (current / max_val))
            pygame.draw.rect(surface, color,
                           (rect.left, rect.top, health_width, rect.height))
        # 테두리
        pygame.draw.rect(surface, Color.WHITE, rect, 1)

    @staticmethod
    def draw_score_display(surface, score, font, color, pos):
        """점수 표시"""
        score_text = font.render(f"Score: {score:,}", True, color)
        surface.blit(score_text, pos)

    @staticmethod
    def fade_color(color, factor):
        """색상 밝기 조절"""
        return tuple(max(0, min(255, int(c * factor))) for c in color)


class Animation:
    """애니메이션 기본 클래스"""

    def __init__(self, duration):
        self.duration = duration
        self.elapsed = 0
        self.finished = False

    def update(self, dt):
        """애니메이션 업데이트"""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.finished = True

    def get_progress(self):
        """진행률 (0.0 ~ 1.0)"""
        return min(1.0, self.elapsed / max(1, self.duration))

    def reset(self):
        """애니메이션 초기화"""
        self.elapsed = 0
        self.finished = False


class FadeAnimation(Animation):
    """페이드 애니메이션"""

    def __init__(self, duration, start_alpha=0, end_alpha=255):
        super().__init__(duration)
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha

    def get_alpha(self):
        """현재 알파값"""
        progress = self.get_progress()
        return int(self.start_alpha + (self.end_alpha - self.start_alpha) * progress)


class ScaleAnimation(Animation):
    """크기 애니메이션"""

    def __init__(self, duration, start_scale=1.0, end_scale=1.5):
        super().__init__(duration)
        self.start_scale = start_scale
        self.end_scale = end_scale

    def get_scale(self):
        """현재 크기"""
        progress = self.get_progress()
        return self.start_scale + (self.end_scale - self.start_scale) * progress
