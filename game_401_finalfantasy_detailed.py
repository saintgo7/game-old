#!/usr/bin/env python3
"""
Final Fantasy - 상세 구현
턴 기반 RPG: 몬스터를 물리치고 강해지며 스토리 진행
"""
import pygame
import random
from enum import Enum
from graphics_themes import Color, Themes

class GameState(Enum):
    """게임 상태"""
    EXPLORATION = 1
    BATTLE = 2
    MENU = 3
    GAME_OVER = 4
    VICTORY = 5


class Character:
    """캐릭터 (플레이어/몬스터)"""

    def __init__(self, name, hp, mp, attack, defense, level=1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.exp = 0

    def take_damage(self, damage):
        """피해 입음"""
        actual_damage = max(1, damage - (self.defense // 2))
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self, amount):
        """회복"""
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        """생존 여부"""
        return self.hp > 0

    def gain_exp(self, amount):
        """경험치 획득"""
        self.exp += amount
        if self.exp >= self.level * 100:
            self.level_up()

    def level_up(self):
        """레벨 업"""
        self.level += 1
        self.exp = 0
        self.max_hp += 20
        self.hp = self.max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack += 5
        self.defense += 3


class FinalFantasyGame:
    """Final Fantasy 상세 구현"""

    def __init__(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.game_name = "Final Fantasy"

        # 플레이어 생성
        self.player = Character("Hero", 100, 50, 15, 8, 1)

        # 게임 상태
        self.state = GameState.EXPLORATION
        self.current_enemy = None
        self.floor = 1
        self.battles_won = 0

        # 테마
        self.theme = Themes.FOREST

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.game_name)

        self.running = True
        self.message = ""
        self.message_time = 0

    def _generate_enemy(self):
        """적 생성"""
        enemy_types = [
            ("Goblin", 20 + self.floor * 5, 0, 8 + self.floor * 2, 2),
            ("Orc", 30 + self.floor * 5, 0, 12 + self.floor * 2, 4),
            ("Troll", 40 + self.floor * 5, 0, 15 + self.floor * 2, 5),
            ("Dragon", 60 + self.floor * 10, 0, 20 + self.floor * 3, 7)
        ]

        name, hp, mp, attack, defense = random.choice(enemy_types)
        self.current_enemy = Character(name, hp, mp, attack, defense, self.floor)

    def _encounter_enemy(self):
        """적 만남"""
        if random.random() < 0.3:  # 30% 확률로 전투
            self._generate_enemy()
            self.state = GameState.BATTLE
            self.message = f"{self.current_enemy.name}과(와) 만났다!"
            self.message_time = pygame.time.get_ticks()

    def _handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.state == GameState.EXPLORATION:
                    if event.key == pygame.K_SPACE:
                        self._encounter_enemy()

                elif self.state == GameState.BATTLE:
                    if event.key == pygame.K_1:  # 공격
                        self._player_attack()
                    elif event.key == pygame.K_2:  # 방어
                        self._player_defend()
                    elif event.key == pygame.K_3:  # 회복
                        self._player_heal()
                    elif event.key == pygame.K_4:  # 도주
                        if random.random() < 0.5:
                            self.state = GameState.EXPLORATION
                            self.message = "전투에서 도망쳤다!"
                        else:
                            self.message = "도망칠 수 없다!"
                        self.message_time = pygame.time.get_ticks()

    def _player_attack(self):
        """플레이어 공격"""
        damage = random.randint(int(self.player.attack * 0.8), int(self.player.attack * 1.2))
        actual_damage = self.current_enemy.take_damage(damage)
        self.message = f"플레이어가 {actual_damage} 데미지를 입혔다!"
        self.message_time = pygame.time.get_ticks()

        if not self.current_enemy.is_alive():
            self._battle_victory()
        else:
            self._enemy_attack()

    def _player_defend(self):
        """플레이어 방어"""
        self.message = "플레이어가 방어했다!"
        self.message_time = pygame.time.get_ticks()
        self._enemy_attack(defender=True)

    def _player_heal(self):
        """플레이어 회복"""
        if self.player.mp >= 10:
            self.player.mp -= 10
            self.player.heal(30)
            self.message = "플레이어가 30 HP를 회복했다!"
            self.message_time = pygame.time.get_ticks()
            self._enemy_attack()
        else:
            self.message = "MP가 부족하다!"
            self.message_time = pygame.time.get_ticks()

    def _enemy_attack(self, defender=False):
        """적 공격"""
        damage = random.randint(int(self.current_enemy.attack * 0.8),
                               int(self.current_enemy.attack * 1.2))

        if defender:
            damage = max(1, damage // 2)

        actual_damage = self.player.take_damage(damage)
        self.message = f"{self.current_enemy.name}이(가) {actual_damage} 데미지를 입혔다!"
        self.message_time = pygame.time.get_ticks()

        if not self.player.is_alive():
            self.state = GameState.GAME_OVER

    def _battle_victory(self):
        """전투 승리"""
        exp_gain = self.current_enemy.level * 50
        self.player.gain_exp(exp_gain)
        self.battles_won += 1
        self.message = f"승리! {exp_gain} 경험치를 얻었다!"
        self.message_time = pygame.time.get_ticks()

        # 10명 물리치면 다음 층
        if self.battles_won % 10 == 0:
            self.floor += 1
            self.battles_won = 0
            self.message = f"다음 층으로 진입했다! (Floor {self.floor})"

        if self.floor > 5:
            self.state = GameState.VICTORY
        else:
            self.state = GameState.EXPLORATION

    def _update(self, dt):
        """게임 업데이트"""
        pass

    def _draw(self, surface):
        """화면 그리기"""
        surface.fill(self.theme.bg_color)

        font_title = pygame.font.Font(None, 48)
        font_normal = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 20)

        if self.state == GameState.EXPLORATION:
            title = font_title.render("던전 탐험", True, self.theme.primary_color)
            surface.blit(title, (self.window_width // 2 - title.get_width() // 2, 50))

            # 플레이어 상태
            info_text = [
                f"이름: {self.player.name}",
                f"레벨: {self.player.level}",
                f"HP: {self.player.hp} / {self.player.max_hp}",
                f"MP: {self.player.mp} / {self.player.max_mp}",
                f"공격: {self.player.attack}, 방어: {self.player.defense}",
                f"",
                f"층: {self.floor}",
                f"",
                "SPACE: 적 만나기",
                "ESC: 종료"
            ]

            for i, text in enumerate(info_text):
                text_surface = font_normal.render(text, True, self.theme.primary_color)
                surface.blit(text_surface, (50, 150 + i * 35))

        elif self.state == GameState.BATTLE:
            # 전투 화면
            title = font_title.render("전투!", True, Color.RED)
            surface.blit(title, (self.window_width // 2 - title.get_width() // 2, 30))

            # 플레이어 정보
            player_info = [
                f"{self.player.name} (Lv.{self.player.level})",
                f"HP: {self.player.hp} / {self.player.max_hp}",
                f"MP: {self.player.mp} / {self.player.max_mp}"
            ]

            for i, text in enumerate(player_info):
                text_surface = font_normal.render(text, True, Color.CYAN)
                surface.blit(text_surface, (50, 120 + i * 40))

            # 적 정보
            enemy_info = [
                f"{self.current_enemy.name} (Lv.{self.current_enemy.level})",
                f"HP: {self.current_enemy.hp} / {self.current_enemy.max_hp}"
            ]

            for i, text in enumerate(enemy_info):
                text_surface = font_normal.render(text, True, Color.RED)
                surface.blit(text_surface, (550, 120 + i * 40))

            # 행동 선택
            actions = [
                "1: 공격",
                "2: 방어",
                "3: 회복",
                "4: 도주"
            ]

            for i, text in enumerate(actions):
                text_surface = font_normal.render(text, True, self.theme.primary_color)
                surface.blit(text_surface, (50, 350 + i * 40))

        elif self.state == GameState.GAME_OVER:
            title = font_title.render("게임 오버", True, Color.RED)
            surface.blit(title, (self.window_width // 2 - title.get_width() // 2, 200))

            message = font_normal.render(f"최종 레벨: {self.player.level}", True, self.theme.primary_color)
            surface.blit(message, (self.window_width // 2 - message.get_width() // 2, 300))

        elif self.state == GameState.VICTORY:
            title = font_title.render("승리!", True, Color.YELLOW)
            surface.blit(title, (self.window_width // 2 - title.get_width() // 2, 200))

            message = font_normal.render(f"최종 레벨: {self.player.level}, 층: {self.floor}", True, self.theme.primary_color)
            surface.blit(message, (self.window_width // 2 - message.get_width() // 2, 300))

        # 메시지 표시
        if pygame.time.get_ticks() - self.message_time < 2000:
            message_surface = font_small.render(self.message, True, Color.WHITE)
            surface.blit(message_surface, (self.window_width // 2 - message_surface.get_width() // 2,
                                          self.window_height - 50))

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
    game = FinalFantasyGame()
    game.run()
