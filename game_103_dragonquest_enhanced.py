#!/usr/bin/env python3
"""
🏰 Dragon Quest (게임 103) - 상세 구현
클래식 RPG로, 플레이어가 캐릭터를 조종하여 몬스터를 격퇴하고
경험치를 쌓아 성장하며 마을을 탐험
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rpg_game_template import RPGGame, Player, Enemy, NPC
from graphics_themes import Color

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class DragonQuestGame(RPGGame):
    """Dragon Quest 게임 - RPG 템플릿 확장"""

    def __init__(self):
        super().__init__("Dragon Quest")

        # Dragon Quest 특화 설정
        self.player = Player("Loto")
        self.player.max_hp = 150
        self.player.hp = 150
        self.player.attack = 15
        self.player.level = 1

        # NPC 추가
        self.npcs = [
            NPC(150, 200, "마왕", "나는 마왕이다!"),
            NPC(400, 200, "현자", "용사여, 마왕을 무찌르길"),
            NPC(600, 150, "상인", "마법의 검을 팔고 있네요"),
        ]

        # 게임 특화
        self.quest_monsters = 3  # 잡아야 할 몬스터 수
        self.monsters_defeated = 0
        self.battle_log = []

    def _check_interactions(self):
        """Dragon Quest 특화: 이벤트 처리"""
        # NPC 상호작용
        for npc in self.npcs:
            if self._rect_collision(
                self.player.x, self.player.y, self.player.width, self.player.height,
                npc.x, npc.y, npc.width, npc.height
            ):
                npc.is_talking = True

        # 무작위 몬스터 만남 (더 자주)
        if random.random() < 0.003:
            self.in_battle = True
            monster_types = ["슬라임", "고블린", "늑대", "드래곤"]
            monster_name = random.choice(monster_types)
            monster_hp = 20 + (self.player.level * 10)
            self.current_enemy = Enemy(0, 0, monster_name, monster_hp, 5 + self.player.level)
            self.battle_log.append(f"{monster_name}이(가) 나타났다!")

    def update(self):
        """Dragon Quest 특화 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        keys = pygame.key.get_pressed()
        self.handle_input(keys)

        # 배틀 상태
        if self.in_battle and self.current_enemy:
            # 자동 전투
            if random.random() < 0.25:
                damage = random.randint(5, 15) + self.player.attack
                if self.current_enemy.take_damage(damage):
                    # 승리
                    exp_gained = 50 + (self.player.level * 20)
                    gold_gained = 50 + (self.player.level * 10)
                    self.player.gain_exp(exp_gained)
                    self.player.gold += gold_gained
                    self.monsters_defeated += 1
                    self.score += 100
                    self.battle_log.append(f"{self.current_enemy.name}을(를) 격퇴했다! {exp_gained} EXP 획득")
                    self.in_battle = False
                    self.current_enemy = None

            # 적 공격
            if random.random() < 0.25:
                enemy_damage = random.randint(3, 10)
                actual_damage = self.player.take_damage(enemy_damage)
                self.battle_log.append(f"{self.current_enemy.name}의 공격! {actual_damage} 피해")
                if self.player.hp <= 0:
                    self.game_state.game_over = True
                    self.battle_log.append("쓰러졌다...")

        # 클리어 조건
        if self.monsters_defeated >= self.quest_monsters:
            self.game_state.game_over = True
            self.score += 1000

    def draw(self):
        """Dragon Quest 특화: 게임 오버레이"""
        super().draw()

        # 배틀 로그 표시
        if self.battle_log:
            log_x = 50
            log_y = SCREEN_HEIGHT - 120
            pygame.draw.rect(self.screen, self.theme.secondary_color,
                           (log_x, log_y, SCREEN_WIDTH - 100, 100), 2)

            for i, log_entry in enumerate(self.battle_log[-3:]):
                log_text = self.small_font.render(log_entry, True, self.theme.text_color)
                self.screen.blit(log_text, (log_x + 10, log_y + 10 + i * 25))

        # 퀘스트 진행도
        quest_text = self.font.render(f"Quest: {self.monsters_defeated}/{self.quest_monsters}", True, Color.GREEN)
        self.screen.blit(quest_text, (SCREEN_WIDTH - 250, 100))

if __name__ == "__main__":
    game = DragonQuestGame()
    game.run()
