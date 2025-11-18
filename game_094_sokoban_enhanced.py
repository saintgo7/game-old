#!/usr/bin/env python3
"""
🧩 Sokoban (게임 094) - 상세 구현
클래식 퍼즐 게임으로, 플레이어가 상자를 지정된 위치로 밀어넣는 게임
"""

import pygame
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from puzzle_game_template import PuzzleGame
from graphics_themes import Color

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class SokobanGame(PuzzleGame):
    """Sokoban 게임 - 퍼즐 템플릿 확장"""

    def __init__(self):
        super().__init__("Sokoban")

        # Sokoban 특화 설정
        self.player_x = 2
        self.player_y = 2
        self.player_size = 30

        # 박스와 대상 위치
        self.boxes = [(4, 2), (5, 2)]
        self.targets = [(4, 4), (5, 4)]
        self.completed_boxes = set()

        self.level = 1
        self.max_moves = 50

    def handle_input(self, keys):
        """Sokoban 특화: 플레이어 이동 및 박스 밀기"""
        if keys[pygame.K_LEFT]:
            self._try_move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            self._try_move(1, 0)
        elif keys[pygame.K_UP]:
            self._try_move(0, -1)
        elif keys[pygame.K_DOWN]:
            self._try_move(0, 1)

    def _try_move(self, dx, dy):
        """이동 시도"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # 경계 체크
        if not (0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height):
            return

        # 박스 체크
        if (new_x, new_y) in self.boxes:
            # 박스 밀기
            box_new_x = new_x + dx
            box_new_y = new_y + dy

            if (0 <= box_new_x < self.grid_width and 0 <= box_new_y < self.grid_height):
                if (box_new_x, box_new_y) not in self.boxes:
                    # 박스 밀기 성공
                    box_idx = self.boxes.index((new_x, new_y))
                    self.boxes[box_idx] = (box_new_x, box_new_y)
                    self.player_x = new_x
                    self.player_y = new_y
                    self.moves += 1
                    self.score += 5

                    # 대상에 도달한 박스 추적
                    if (box_new_x, box_new_y) in self.targets:
                        self.completed_boxes.add((box_new_x, box_new_y))
                        self.score += 50
        else:
            # 일반 이동
            self.player_x = new_x
            self.player_y = new_y
            self.moves += 1

    def _check_win(self):
        """승리 조건: 모든 박스가 대상에 위치"""
        return len(self.completed_boxes) == len(self.targets)

    def update(self):
        """Sokoban 특화 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        keys = pygame.key.get_pressed()
        self.handle_input(keys)

        if self._check_win():
            self.game_state.game_over = True
            self.score += (self.max_moves - self.moves) * 10

        if self.moves >= self.max_moves:
            self.game_state.game_over = True

    def draw(self):
        """Sokoban 특화: 박스와 대상 표시"""
        self.screen.fill(self.theme.bg_color)

        # 제목
        title_text = self.font.render("Sokoban", True, self.theme.text_color)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - 80, 20))

        # 게임 영역
        grid_x = 50
        grid_y = 100
        cell_size = 40

        # 그리드 배경
        pygame.draw.rect(self.screen, self.theme.secondary_color,
                        (grid_x, grid_y, self.grid_width * cell_size, self.grid_height * cell_size), 2)

        # 셀 그리기
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell_x = grid_x + x * cell_size
                cell_y = grid_y + y * cell_size
                pygame.draw.rect(self.screen, self.theme.secondary_color,
                               (cell_x, cell_y, cell_size, cell_size), 1)

        # 대상 위치 표시
        for tx, ty in self.targets:
            cell_x = grid_x + tx * cell_size + cell_size // 2
            cell_y = grid_y + ty * cell_size + cell_size // 2
            pygame.draw.circle(self.screen, Color.CYAN, (cell_x, cell_y), 8, 2)

        # 박스 표시
        for bx, by in self.boxes:
            cell_x = grid_x + bx * cell_size
            cell_y = grid_y + by * cell_size
            color = Color.GREEN if (bx, by) in self.completed_boxes else Color.YELLOW
            pygame.draw.rect(self.screen, color, (cell_x + 5, cell_y + 5, cell_size - 10, cell_size - 10))

        # 플레이어 표시
        player_x = grid_x + self.player_x * cell_size + cell_size // 2
        player_y = grid_y + self.player_y * cell_size + cell_size // 2
        pygame.draw.circle(self.screen, Color.BLUE, (player_x, player_y), 12)

        # 정보 표시
        info_x = grid_x + self.grid_width * cell_size + 50
        score_text = self.small_font.render(f"Score: {self.score}", True, self.theme.text_color)
        self.screen.blit(score_text, (info_x, 120))

        moves_text = self.small_font.render(f"Moves: {self.moves}/{self.max_moves}", True, self.theme.text_color)
        self.screen.blit(moves_text, (info_x, 150))

        completed_text = self.small_font.render(f"Boxes: {len(self.completed_boxes)}/{len(self.targets)}", True, self.theme.text_color)
        self.screen.blit(completed_text, (info_x, 180))

        if self.game_state.game_over and self._check_win():
            win_text = self.font.render("LEVEL CLEAR!", True, Color.GREEN)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    game = SokobanGame()
    game.run()
