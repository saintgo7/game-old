#!/usr/bin/env python3
"""
🏰 RPG 게임 템플릿
Dragon Quest, Ultima, Final Fantasy 등 RPG의 기본 구현
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from game_utils import ScoreManager, GameConfig, GameState
from sound_manager import SoundManager
from graphics_themes import Themes, Color

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class Player:
    """플레이어 캐릭터"""
    def __init__(self, name="Hero"):
        self.name = name
        self.x = 100
        self.y = 100
        self.width = 30
        self.height = 40
        self.speed = 3

        # 스탯
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.attack = 10
        self.defense = 5

        # 인벤토리
        self.inventory = ["검", "포션"]
        self.gold = 100

    def gain_exp(self, amount):
        """경험치 획득"""
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        """레벨 업"""
        self.level += 1
        self.exp = 0
        self.exp_to_level = int(self.exp_to_level * 1.2)
        self.max_hp += 20
        self.hp = self.max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack += 5
        self.defense += 2

    def take_damage(self, damage):
        """피해 입음"""
        actual_damage = max(1, damage - self.defense // 2)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self, amount):
        """회복"""
        self.hp = min(self.max_hp, self.hp + amount)

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, theme.primary_color, rect)

class NPC:
    """NPC"""
    def __init__(self, x, y, name, dialogue):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 30
        self.name = name
        self.dialogue = dialogue
        self.is_talking = False

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, Color.GREEN, rect)

class Enemy:
    """적"""
    def __init__(self, x, y, name="Monster", hp=30, attack=5):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.exp_reward = 50
        self.gold_reward = random.randint(10, 50)

    def take_damage(self, damage):
        """피해 입음"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, Color.RED, rect)

class RPGGame:
    """RPG 기본 클래스"""
    def __init__(self, game_name):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"🏰 {game_name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)

        # 매니저
        self.score_manager = ScoreManager(game_name.lower().replace(" ", "_"))
        self.config = GameConfig(game_name.lower().replace(" ", "_"))
        self.sound_manager = SoundManager()
        self.game_state = GameState()

        # 테마
        theme_name = self.config.get("theme", "classic")
        self.theme = getattr(Themes, theme_name.upper(), Themes.CLASSIC)

        # 게임 상태
        self.running = True
        self.paused = False
        self.in_battle = False
        self.score = 0

        # 플레이어
        self.player = Player("Hero")

        # 맵 NPC들
        self.npcs = [
            NPC(200, 150, "상인", "무기와 포션을 팝니다"),
            NPC(400, 200, "마법사", "마법을 배워보세요"),
        ]

        # 적
        self.enemies = []
        self.current_enemy = None

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE:
                    self._new_game()

    def handle_input(self, keys):
        """플레이어 입력"""
        if self.in_battle:
            return

        if keys[pygame.K_LEFT]:
            self.player.x = max(0, self.player.x - self.player.speed)
        if keys[pygame.K_RIGHT]:
            self.player.x = min(SCREEN_WIDTH - self.player.width, self.player.x + self.player.speed)
        if keys[pygame.K_UP]:
            self.player.y = max(0, self.player.y - self.player.speed)
        if keys[pygame.K_DOWN]:
            self.player.y = min(SCREEN_HEIGHT - self.player.height, self.player.y + self.player.speed)

        # 이동 시 적과의 상호작용
        self._check_interactions()

    def _check_interactions(self):
        """상호작용 체크"""
        # NPC 상호작용
        for npc in self.npcs:
            if self._rect_collision(
                self.player.x, self.player.y, self.player.width, self.player.height,
                npc.x, npc.y, npc.width, npc.height
            ):
                npc.is_talking = True

        # 적 만남
        if random.random() < 0.001:  # 매우 낮은 확률로 적 만남
            self.in_battle = True
            self.current_enemy = Enemy(0, 0, "슬라임", 20, 3)

    def _rect_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        """충돌 검사"""
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        keys = pygame.key.get_pressed()
        self.handle_input(keys)

        # 배틀 상태
        if self.in_battle and self.current_enemy:
            # 자동 전투 (간단한 구현)
            if random.random() < 0.3:
                damage = random.randint(5, 15)
                if self.current_enemy.take_damage(damage):
                    # 승리
                    self.player.gain_exp(self.current_enemy.exp_reward)
                    self.player.gold += self.current_enemy.gold_reward
                    self.score += 100
                    self.in_battle = False
                    self.current_enemy = None

            # 적 공격
            if random.random() < 0.3:
                enemy_damage = random.randint(1, 10)
                self.player.take_damage(enemy_damage)
                if self.player.hp <= 0:
                    self.game_state.game_over = True

    def _new_game(self):
        """새 게임"""
        self.player = Player("Hero")
        self.in_battle = False
        self.score = 0

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 배경
        pygame.draw.rect(self.screen, self.theme.secondary_color,
                        pygame.Rect(50, 100, 700, 400), 1)

        # NPC 그리기
        for npc in self.npcs:
            npc.draw(self.screen, self.theme)

        # 플레이어 그리기
        self.player.draw(self.screen, self.theme)

        # 적 그리기
        if self.in_battle and self.current_enemy:
            self.current_enemy.draw(self.screen, self.theme)

        # UI - 플레이어 정보
        ui_x = SCREEN_WIDTH - 250
        info_texts = [
            f"Level: {self.player.level}",
            f"HP: {self.player.hp}/{self.player.max_hp}",
            f"MP: {self.player.mp}/{self.player.max_mp}",
            f"EXP: {self.player.exp}/{self.player.exp_to_level}",
            f"Gold: {self.player.gold}",
            f"ATK: {self.player.attack} DEF: {self.player.defense}",
        ]

        for i, text in enumerate(info_texts):
            text_surface = self.small_font.render(text, True, self.theme.text_color)
            self.screen.blit(text_surface, (ui_x, 20 + i * 25))

        # 배틀 UI
        if self.in_battle and self.current_enemy:
            battle_text = self.font.render("배틀 중!", True, Color.RED)
            self.screen.blit(battle_text, (SCREEN_WIDTH // 2 - 50, 50))

            enemy_info = f"{self.current_enemy.name} - HP: {self.current_enemy.hp}/{self.current_enemy.max_hp}"
            enemy_text = self.small_font.render(enemy_info, True, self.theme.text_color)
            self.screen.blit(enemy_text, (SCREEN_WIDTH // 2 - 100, 100))

        pygame.display.flip()

    def run(self):
        """게임 실행"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # 점수 저장
        if self.score > 0:
            rank = self.score_manager.add_score(
                self.config.get("player_name", "Player"),
                self.score
            )

        pygame.quit()
