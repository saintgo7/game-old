#!/usr/bin/env python3
"""
그래픽 테마 및 디자인 시스템 (향상된 버전)
- 파티클 이펙트 시스템
- 고급 애니메이션
- 시각 효과
"""
import pygame
import math
import random
from typing import Tuple, List
from enum import Enum

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


class RotateAnimation(Animation):
    """회전 애니메이션"""

    def __init__(self, duration, start_angle=0, end_angle=360):
        super().__init__(duration)
        self.start_angle = start_angle
        self.end_angle = end_angle

    def get_angle(self):
        """현재 각도"""
        progress = self.get_progress()
        return self.start_angle + (self.end_angle - self.start_angle) * progress


class MoveAnimation(Animation):
    """이동 애니메이션"""

    def __init__(self, duration, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        super().__init__(duration)
        self.start_pos = start_pos
        self.end_pos = end_pos

    def get_position(self):
        """현재 위치"""
        progress = self.get_progress()
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        return (int(x), int(y))


# 파티클 시스템
class Particle:
    """개별 파티클"""

    def __init__(self, x, y, vx, vy, color, size=5, lifetime=1000):
        self.x = x
        self.y = y
        self.vx = vx  # x 속도
        self.vy = vy  # y 속도
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.alive = True

    def update(self, dt):
        """파티클 업데이트"""
        self.age += dt
        if self.age >= self.lifetime:
            self.alive = False
            return

        # 중력 적용
        self.vy += 0.3  # 중력 가속도

        # 위치 업데이트
        self.x += self.vx * (dt / 1000.0)
        self.y += self.vy * (dt / 1000.0)

    def draw(self, surface):
        """파티클 그리기"""
        if not self.alive:
            return

        # 나이에 따라 투명도 감소
        progress = self.age / self.lifetime
        alpha = int(255 * (1 - progress))

        try:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
        except:
            pass


class ParticleSystem:
    """파티클 이펙트 시스템"""

    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x, y, count=10, speed_range=(1, 5), color=Color.WHITE,
             angle_range=None, lifetime=1000):
        """파티클 방출"""
        if angle_range is None:
            angle_range = (0, 360)

        for _ in range(count):
            angle = random.uniform(math.radians(angle_range[0]),
                                  math.radians(angle_range[1]))
            speed = random.uniform(speed_range[0], speed_range[1])

            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            particle = Particle(x, y, vx, vy, color, size=5, lifetime=lifetime)
            self.particles.append(particle)

    def emit_explosion(self, x, y, color=Color.YELLOW, count=20):
        """폭발 파티클 방출"""
        self.emit(x, y, count=count, speed_range=(2, 8),
                 color=color, angle_range=(0, 360), lifetime=800)

    def emit_smoke(self, x, y, count=5):
        """연기 파티클 방출"""
        self.emit(x, y, count=count, speed_range=(0.5, 2),
                 color=Color.GRAY, angle_range=(0, 360), lifetime=1500)

    def emit_sparkle(self, x, y, color=Color.WHITE, count=15):
        """반짝임 파티클 방출"""
        self.emit(x, y, count=count, speed_range=(1, 3),
                 color=color, angle_range=(0, 360), lifetime=600)

    def emit_directional(self, x, y, angle, spread=45, count=10,
                        speed_range=(2, 5), color=Color.WHITE):
        """방향성 파티클 방출"""
        angle_range = (angle - spread/2, angle + spread/2)
        self.emit(x, y, count=count, speed_range=speed_range,
                 color=color, angle_range=angle_range, lifetime=800)

    def update(self, dt):
        """전체 파티클 업데이트"""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, surface):
        """전체 파티클 그리기"""
        for particle in self.particles:
            particle.draw(surface)

    def clear(self):
        """모든 파티클 제거"""
        self.particles.clear()

    def is_active(self):
        """활성 파티클이 있는지 확인"""
        return len(self.particles) > 0
