#!/usr/bin/env python3
"""
🥊 스포츠/격투 게임 템플릿
Tekken, Mortal Kombat, Street Fighter, Boxing, Tennis 등 스포츠 및 격투 게임의 기본 구현
"""

import pygame
import random
import sys
from pathlib import Path
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))

from game_utils import ScoreManager, GameConfig, GameState
from sound_manager import SoundManager
from graphics_themes import Themes, Color

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

class GameDifficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4

class Fighter:
    """격투가/선수"""
    def __init__(self, x, y, is_player=False, name="Fighter"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.name = name
        self.is_player = is_player

        # 스탯
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 15
        self.defense = 5
        self.speed = 4

        # 전투 상태
        self.combo_count = 0
        self.combo_timer = 0
        self.max_combo = 5
        self.is_attacking = False
        self.attack_cooldown = 0
        self.is_blocking = False
        self.block_cooldown = 0

        # 특수 이동
        self.special_cooldown = 0
        self.special_max_cooldown = 120  # 2초

    def take_damage(self, damage, is_special=False):
        """피해 입음"""
        if self.is_blocking:
            damage = int(damage * 0.5)  # 블록 시 50% 감소

        actual_damage = max(1, damage - self.defense // 3)
        self.hp = max(0, self.hp - actual_damage)

        if actual_damage > 0:
            self.combo_count = 0
            self.combo_timer = 0

        return self.hp <= 0

    def heal(self, amount):
        """회복"""
        self.hp = min(self.max_hp, self.hp + amount)

    def perform_attack(self, target, combo_multiplier=1.0):
        """공격"""
        if self.attack_cooldown <= 0:
            damage = int(self.attack * combo_multiplier)
            target.take_damage(damage)
            self.attack_cooldown = 15
            self.combo_count += 1
            self.combo_timer = 60
            return True
        return False

    def perform_special_attack(self, target):
        """특수 공격"""
        if self.special_cooldown <= 0:
            damage = int(self.attack * 2.5)
            target.take_damage(damage, is_special=True)
            self.special_cooldown = self.special_max_cooldown
            self.combo_count = 0
            return True
        return False

    def toggle_block(self, blocking):
        """방어"""
        self.is_blocking = blocking

    def move(self, direction):
        """이동 (방향: -1 왼쪽, 1 오른쪽)"""
        new_x = self.x + direction * self.speed
        if 0 <= new_x <= SCREEN_WIDTH - self.width:
            self.x = new_x

    def update(self):
        """업데이트"""
        # 쿨다운 감소
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0

    def draw(self, surface, theme, opponent_x):
        """그리기"""
        # 격투가 몸
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, theme.primary_color, rect)

        # 공격 표시
        if self.attack_cooldown > 30:
            pygame.draw.rect(surface, Color.YELLOW, rect, 3)

        # 방어 표시
        if self.is_blocking:
            pygame.draw.circle(surface, Color.CYAN, (int(self.x + self.width // 2), int(self.y + self.height // 2)), 35, 3)

class AIFighter:
    """AI 격투가"""
    def __init__(self, x, y, difficulty=GameDifficulty.NORMAL):
        self.fighter = Fighter(x, y, is_player=False)
        self.difficulty = difficulty
        self.decision_timer = 0
        self.decision_interval = 30
        self.current_action = None

    def update(self, player):
        """AI 업데이트"""
        self.fighter.update()
        self.decision_timer -= 1

        if self.decision_timer <= 0:
            self.decide_action(player)
            self.decision_timer = self.decision_interval

        self.execute_action(player)

    def decide_action(self, player):
        """행동 결정"""
        distance = abs(self.fighter.x - player.x)

        if self.difficulty == GameDifficulty.EASY:
            choice = random.random()
            if choice < 0.3:
                self.current_action = "move_toward"
            elif choice < 0.6:
                self.current_action = "attack"
            else:
                self.current_action = "idle"
        elif self.difficulty == GameDifficulty.NORMAL:
            if distance > 100 and random.random() < 0.4:
                self.current_action = "move_toward"
            elif self.fighter.hp < 40 and random.random() < 0.3:
                self.current_action = "block"
            elif random.random() < 0.5:
                self.current_action = "attack"
            else:
                self.current_action = "idle"
        elif self.difficulty == GameDifficulty.HARD:
            if distance < 50 and self.fighter.special_cooldown == 0 and random.random() < 0.4:
                self.current_action = "special"
            elif distance > 100:
                self.current_action = "move_toward"
            elif self.fighter.hp < 30:
                self.current_action = "block"
            else:
                self.current_action = "attack"
        else:  # EXTREME
            if distance < 50 and self.fighter.special_cooldown == 0 and random.random() < 0.6:
                self.current_action = "special"
            elif player.hp > 50 and distance > 80:
                self.current_action = "move_toward"
            elif self.fighter.hp < 50:
                self.current_action = "block"
            else:
                self.current_action = "attack"

    def execute_action(self, player):
        """행동 실행"""
        if self.current_action == "move_toward":
            if self.fighter.x < player.x - 30:
                self.fighter.move(1)
            elif self.fighter.x > player.x + 30:
                self.fighter.move(-1)
        elif self.current_action == "attack":
            combo_mult = 1.0 + (self.fighter.combo_count * 0.2)
            self.fighter.perform_attack(player, combo_mult)
        elif self.current_action == "special":
            self.fighter.perform_special_attack(player)
        elif self.current_action == "block":
            self.fighter.toggle_block(True)
        else:  # idle
            self.fighter.toggle_block(False)

class SportsGame:
    """스포츠/격투 게임 기본 클래스"""
    def __init__(self, game_name, difficulty=GameDifficulty.NORMAL):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"🥊 {game_name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

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
        self.difficulty = difficulty
        self.score = 0
        self.round_num = 1
        self.round_time = 180  # 3분
        self.round_timer = self.round_time

        # 플레이어와 AI
        self.player = Fighter(100, SCREEN_HEIGHT - 150, is_player=True, name="Player")
        self.opponent = AIFighter(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 150, difficulty).fighter
        self.ai = AIFighter(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 150, difficulty)

        # 라운드 관리
        self.rounds_won = [0, 0]  # [플레이어, 상대]

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
                    self._new_round()

    def handle_input(self, keys):
        """플레이어 입력"""
        # 이동
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)

        # 공격
        if keys[pygame.K_z]:
            combo_mult = 1.0 + (self.player.combo_count * 0.2)
            self.player.perform_attack(self.opponent, combo_mult)

        # 특수 공격
        if keys[pygame.K_x]:
            self.player.perform_special_attack(self.opponent)

        # 방어
        self.player.toggle_block(keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        # 라운드 시간 감소
        if self.round_timer > 0:
            self.round_timer -= 1

        # 플레이어 입력
        keys = pygame.key.get_pressed()
        self.handle_input(keys)

        # 플레이어 업데이트
        self.player.update()

        # AI 업데이트
        self.ai.update(self.player)

        # 라운드 종료 체크
        if self.round_timer <= 0 or self.player.hp <= 0 or self.opponent.hp <= 0:
            self._end_round()

    def _end_round(self):
        """라운드 종료"""
        # 승자 결정
        if self.player.hp > self.opponent.hp:
            self.rounds_won[0] += 1
            self.score += 500
        elif self.opponent.hp > self.player.hp:
            self.rounds_won[1] += 1
        else:
            # 동점
            self.score += 250

        # 3라운드 후 게임 종료
        if self.round_num >= 3 or self.rounds_won[0] >= 2 or self.rounds_won[1] >= 2:
            self.game_state.game_over = True
        else:
            self._new_round()

    def _new_round(self):
        """새 라운드"""
        self.round_num += 1
        self.round_timer = self.round_time
        self.player = Fighter(100, SCREEN_HEIGHT - 150, is_player=True, name="Player")
        self.opponent = AIFighter(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 150, self.difficulty).fighter
        self.ai = AIFighter(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 150, self.difficulty)

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 경기장 배경
        pygame.draw.rect(self.screen, self.theme.secondary_color,
                        pygame.Rect(50, 50, SCREEN_WIDTH - 100, 300), 2)

        # 격투가 그리기
        self.player.draw(self.screen, self.theme, self.opponent.x)
        self.opponent.draw(self.screen, self.theme, self.player.x)

        # 체력 표시
        hp_y = 20
        # 플레이어 체력
        player_hp_ratio = max(0, self.player.hp / self.player.max_hp)
        pygame.draw.rect(self.screen, Color.RED, (50, hp_y, 200, 20))
        pygame.draw.rect(self.screen, Color.GREEN, (50, hp_y, 200 * player_hp_ratio, 20))
        pygame.draw.rect(self.screen, Color.WHITE, (50, hp_y, 200, 20), 2)

        player_hp_text = self.small_font.render(f"Player: {int(self.player.hp)}/{int(self.player.max_hp)}", True, self.theme.text_color)
        self.screen.blit(player_hp_text, (60, hp_y + 25))

        # 상대 체력
        opponent_hp_ratio = max(0, self.opponent.hp / self.opponent.max_hp)
        pygame.draw.rect(self.screen, Color.RED, (SCREEN_WIDTH - 250, hp_y, 200, 20))
        pygame.draw.rect(self.screen, Color.GREEN, (SCREEN_WIDTH - 250, hp_y, 200 * opponent_hp_ratio, 20))
        pygame.draw.rect(self.screen, Color.WHITE, (SCREEN_WIDTH - 250, hp_y, 200, 20), 2)

        opponent_hp_text = self.small_font.render(f"Opponent: {int(self.opponent.hp)}/{int(self.opponent.max_hp)}", True, self.theme.text_color)
        self.screen.blit(opponent_hp_text, (SCREEN_WIDTH - 240, hp_y + 25))

        # 라운드 정보
        round_text = self.font.render(f"Round {self.round_num}", True, self.theme.text_color)
        self.screen.blit(round_text, (SCREEN_WIDTH // 2 - 60, 20))

        time_text = self.small_font.render(f"Time: {self.round_timer // 60}:{self.round_timer % 60:02d}", True, self.theme.text_color)
        self.screen.blit(time_text, (SCREEN_WIDTH // 2 - 40, 60))

        # 스코어
        score_text = self.font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 60))

        # 라운드 스코어
        rounds_text = self.small_font.render(f"Rounds Won: {self.rounds_won[0]} - {self.rounds_won[1]}", True, self.theme.text_color)
        self.screen.blit(rounds_text, (10, SCREEN_HEIGHT - 30))

        # 콤보 표시
        if self.player.combo_count > 1:
            combo_text = self.font.render(f"COMBO x{self.player.combo_count}!", True, Color.YELLOW)
            self.screen.blit(combo_text, (SCREEN_WIDTH // 2 - 80, 150))

        # 컨트롤 정보
        controls = [
            "LEFT/RIGHT: Move",
            "Z: Attack",
            "X: Special",
            "CTRL: Block",
            "P: Pause"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, self.theme.text_color)
            self.screen.blit(control_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150 + i * 25))

        # 일시정지
        if self.paused:
            pause_text = self.font.render("PAUSED", True, Color.RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # 게임 오버
        if self.game_state.game_over:
            winner = "Player Wins!" if self.rounds_won[0] >= 2 else "Opponent Wins!" if self.rounds_won[1] >= 2 else "Draw!"
            over_text = self.font.render(winner, True, Color.GREEN if self.rounds_won[0] >= 2 else Color.RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

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
