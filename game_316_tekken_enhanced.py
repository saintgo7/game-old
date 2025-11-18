#!/usr/bin/env python3
"""
🥊 Tekken (게임 316) - 상세 구현
격투 게임으로, 플레이어가 캐릭터를 선택하여 상대 격투가와 대전하고
연타 콤보와 특수 기술을 활용하여 승리
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sports_game_template import SportsGame, GameDifficulty
from graphics_themes import Color

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class TekkenGame(SportsGame):
    """Tekken 게임 - 스포츠 템플릿 확장"""

    def __init__(self):
        super().__init__("Tekken", difficulty=GameDifficulty.NORMAL)

        # Tekken 특화 설정
        self.player.name = "Kazuya"
        self.opponent.name = "Paul"

        # 캐릭터 스탯 조정
        self.player.max_hp = 120
        self.player.hp = 120
        self.player.attack = 18
        self.opponent.max_hp = 120
        self.opponent.hp = 120
        self.opponent.attack = 16

        # Tekken 특화
        self.move_counter = 0
        self.last_move = None
        self.special_moves = {
            "hadouken": {"damage": 30, "cooldown": 60, "current": 0},
            "uppercut": {"damage": 25, "cooldown": 40, "current": 0},
            "sweep": {"damage": 20, "cooldown": 30, "current": 0},
        }

    def handle_input(self, keys):
        """Tekken 특화: 특수 기술 입력"""
        # 기본 입력
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)

        # 공격 버튼
        if keys[pygame.K_z]:
            combo_mult = 1.0 + (self.player.combo_count * 0.25)
            self.player.perform_attack(self.opponent, combo_mult)
            self.move_counter += 1

        # 특수 기술 (1, 2, 3 키)
        if keys[pygame.K_1] and self.special_moves["hadouken"]["current"] <= 0:
            damage = self.special_moves["hadouken"]["damage"]
            self.opponent.take_damage(damage, is_special=True)
            self.special_moves["hadouken"]["current"] = self.special_moves["hadouken"]["cooldown"]
            self.score += 150
            self.player.combo_count += 2

        elif keys[pygame.K_2] and self.special_moves["uppercut"]["current"] <= 0:
            damage = self.special_moves["uppercut"]["damage"]
            self.opponent.take_damage(damage, is_special=True)
            self.special_moves["uppercut"]["current"] = self.special_moves["uppercut"]["cooldown"]
            self.score += 120
            self.player.combo_count += 1

        elif keys[pygame.K_3] and self.special_moves["sweep"]["current"] <= 0:
            damage = self.special_moves["sweep"]["damage"]
            self.opponent.take_damage(damage, is_special=True)
            self.special_moves["sweep"]["current"] = self.special_moves["sweep"]["cooldown"]
            self.score += 100

        # 방어
        self.player.toggle_block(keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])

        # 특수 기술 쿨다운 감소
        for move in self.special_moves.values():
            move["current"] = max(0, move["current"] - 1)

    def update(self):
        """Tekken 특화 업데이트"""
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

    def draw(self):
        """Tekken 특화: 콤보 카운터와 특수 기술 표시"""
        super().draw()

        # 특수 기술 쿨다운 표시
        skill_x = 10
        skill_y = SCREEN_HEIGHT - 100

        skill_info = [
            ("1-Hadouken", self.special_moves["hadouken"]),
            ("2-Uppercut", self.special_moves["uppercut"]),
            ("3-Sweep", self.special_moves["sweep"]),
        ]

        for i, (name, move) in enumerate(skill_info):
            cooldown_ratio = 1.0 - (move["current"] / move["cooldown"]) if move["cooldown"] > 0 else 1.0
            color = Color.GREEN if move["current"] == 0 else Color.YELLOW

            pygame.draw.rect(self.screen, Color.RED, (skill_x, skill_y + i * 25, 100, 20))
            pygame.draw.rect(self.screen, color, (skill_x, skill_y + i * 25, 100 * cooldown_ratio, 20))
            pygame.draw.rect(self.screen, Color.WHITE, (skill_x, skill_y + i * 25, 100, 20), 2)

            skill_text = self.small_font.render(name, True, self.theme.text_color)
            self.screen.blit(skill_text, (skill_x + 110, skill_y + i * 25 + 2))

        # 플레이어 이동 카운트
        moves_text = self.small_font.render(f"Moves: {self.move_counter}", True, self.theme.text_color)
        self.screen.blit(moves_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 100))

if __name__ == "__main__":
    game = TekkenGame()
    game.run()
