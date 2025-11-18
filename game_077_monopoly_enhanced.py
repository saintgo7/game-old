#!/usr/bin/env python3
"""
♟️ Monopoly (게임 077) - 상세 구현
클래식 보드 게임으로, 플레이어가 주사위를 굴려 보드를 이동하며
부동산을 구매하고 임금을 받아 부를 축적
"""

import pygame
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from board_game_template import BoardGame, GameDifficulty
from graphics_themes import Color

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

class MonopolyGame(BoardGame):
    """Monopoly 게임 - 보드 템플릿 확장"""

    def __init__(self):
        super().__init__("Monopoly", difficulty=GameDifficulty.NORMAL)

        # Monopoly 특화 설정
        self.board_size = 10  # 10x10 보드
        self.board_start_x = 100
        self.board_start_y = 150
        self.tile_width = 50
        self.tile_height = 50

        # 게임 화폐
        self.player_money = 1500
        self.ai_money = 1500

        # 부동산 (타일 ID -> 소유자 및 가격)
        self.properties = {}
        self.setup_properties()

        # 플레이어 위치
        self.player_pos = 0  # 보드 위의 위치 (0-39)
        self.ai_pos = 0

        # 주사위
        self.dice_result = 0
        self.can_roll = True
        self.round_count = 0

    def setup_properties(self):
        """부동산 초기 설정"""
        property_prices = {
            1: 60, 3: 60, 6: 100, 8: 100, 9: 120,
            11: 140, 13: 140, 14: 160, 16: 180, 18: 200,
            19: 220, 21: 220, 23: 240, 25: 260, 26: 260,
            27: 280, 29: 300, 31: 300, 32: 320, 34: 350,
        }
        for tile_id, price in property_prices.items():
            self.properties[tile_id] = {"price": price, "owner": None, "level": 0}

    def _handle_click(self, pos):
        """마우스 클릭 처리 (주사위 굴리기)"""
        # 주사위 버튼 클릭
        dice_btn_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 120, 50)
        if dice_btn_rect.collidepoint(pos) and self.can_roll and self.current_turn == 0:
            self.roll_dice()
            return

        super()._handle_click(pos)

    def roll_dice(self):
        """주사위 굴리기"""
        self.dice_result = random.randint(1, 6) + random.randint(1, 6)
        self.player_pos = (self.player_pos + self.dice_result) % 40
        self.land_on_tile(self.player_pos, is_player=True)
        self.can_roll = False
        self.current_turn = 1

    def land_on_tile(self, tile_id, is_player=True):
        """타일에 도착"""
        if tile_id not in self.properties:
            return

        prop = self.properties[tile_id]

        if prop["owner"] is None:
            # 구매 가능
            if is_player and self.player_money >= prop["price"]:
                if random.random() < 0.7:  # 70% 확률로 구매
                    self.player_money -= prop["price"]
                    prop["owner"] = 0
                    self.player_score += 100
        else:
            # 임금 지불
            rent = prop["price"] // 10 * (prop["level"] + 1)
            if is_player:
                self.player_money -= rent
                self.ai_money += rent
            else:
                self.ai_money -= rent
                self.player_money += rent

    def _end_turn(self):
        """턴 종료"""
        if self.current_turn == 0:
            self.current_turn = 1
        else:
            self.current_turn = 0
            # AI 턴
            if self.turn_timer <= 0:
                self.ai_pos = (self.ai_pos + random.randint(2, 12)) % 40
                self.land_on_tile(self.ai_pos, is_player=False)
                self.turn_count += 1
                self.turn_timer = 180
                self.can_roll = True

    def update(self):
        """Monopoly 특화 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        self.round_count += 1
        self.turn_timer -= 1

        # AI 턴
        if self.current_turn == 1 and self.turn_timer <= 0:
            self.ai_pos = (self.ai_pos + random.randint(2, 12)) % 40
            self.land_on_tile(self.ai_pos, is_player=False)
            self.turn_count += 1
            self.turn_timer = 180
            self.can_roll = True
            self.current_turn = 0

        # 게임 오버 조건 (파산)
        if self.player_money <= 0 or self.ai_money <= 0:
            self.game_state.game_over = True

        # 또는 턴 수 제한
        if self.round_count >= 300:
            self.game_state.game_over = True

    def draw(self):
        """Monopoly 특화: 보드 표시"""
        self.screen.fill(self.theme.bg_color)

        # 제목
        title_text = self.font.render("Monopoly", True, self.theme.text_color)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 80, 20))

        # 보드 그리기 (단순화된 버전)
        board_x = self.board_start_x
        board_y = self.board_start_y

        # 보드 틀
        pygame.draw.rect(self.screen, Color.GREEN,
                        (board_x - 20, board_y - 20, 500 + 40, 500 + 40), 3)

        # 타일 그리기
        for i in range(40):
            x = board_x
            y = board_y
            size = 50

            # 보드 위치 계산 (사각형 둘레)
            if i < 10:
                x += i * size
            elif i < 20:
                x += 450
                y += (i - 10) * size
            elif i < 30:
                x += 450 - (i - 20) * size
                y += 450
            else:
                y += 450 - (i - 30) * size

            tile_color = self.theme.secondary_color
            if i in self.properties and self.properties[i]["owner"] is not None:
                tile_color = Color.BLUE if self.properties[i]["owner"] == 0 else Color.RED

            pygame.draw.rect(self.screen, tile_color, (x, y, size - 2, size - 2))
            pygame.draw.rect(self.screen, Color.WHITE, (x, y, size - 2, size - 2), 1)

        # 플레이어 표시
        player_x = board_x + (self.player_pos % 10) * 50 + 25
        player_y = board_y + (self.player_pos // 10) * 50 + 25
        pygame.draw.circle(self.screen, Color.BLUE, (int(player_x), int(player_y)), 10)

        # AI 표시
        ai_x = board_x + (self.ai_pos % 10) * 50 + 25
        ai_y = board_y + (self.ai_pos // 10) * 50 + 25
        pygame.draw.circle(self.screen, Color.RED, (int(ai_x), int(ai_y)), 10)

        # 정보 표시
        info_x = SCREEN_WIDTH - 250

        money_text = self.font.render("Money", True, self.theme.text_color)
        self.screen.blit(money_text, (info_x, 100))

        player_money_text = self.small_font.render(f"Player: ${self.player_money}", True, Color.BLUE)
        self.screen.blit(player_money_text, (info_x, 140))

        ai_money_text = self.small_font.render(f"AI: ${self.ai_money}", True, Color.RED)
        self.screen.blit(ai_money_text, (info_x, 170))

        # 주사위 결과
        if self.dice_result > 0:
            dice_text = self.small_font.render(f"Dice: {self.dice_result}", True, self.theme.text_color)
            self.screen.blit(dice_text, (info_x, 210))

        # 턴 정보
        turn_player = "Player" if self.current_turn == 0 else "AI"
        turn_text = self.small_font.render(f"Turn: {turn_player}", True,
                                          Color.BLUE if self.current_turn == 0 else Color.RED)
        self.screen.blit(turn_text, (info_x, 250))

        # 주사위 버튼
        dice_btn = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 120, 50)
        btn_color = Color.GREEN if self.can_roll and self.current_turn == 0 else Color.GRAY
        pygame.draw.rect(self.screen, btn_color, dice_btn)
        pygame.draw.rect(self.screen, Color.WHITE, dice_btn, 2)
        btn_text = self.small_font.render("Roll Dice", True, Color.WHITE)
        self.screen.blit(btn_text, (SCREEN_WIDTH - 140, SCREEN_HEIGHT - 90))

        # 게임 오버
        if self.game_state.game_over:
            winner = "Player Wins!" if self.player_money > self.ai_money else "AI Wins!"
            over_text = self.font.render(winner, True, Color.GREEN if self.player_money > self.ai_money else Color.RED)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

if __name__ == "__main__":
    game = MonopolyGame()
    game.run()
