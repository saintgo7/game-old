#!/usr/bin/env python3
"""
🎮 클래식 아케이드 게임 런처 (Arcade Launcher)
모든 게임을 한 곳에서 관리하고 실행하는 중앙 프로그램
"""

import pygame
import subprocess
import sys
import os
from pathlib import Path
from enum import Enum

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
FPS = 60

class Color:
    """색상 정의"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 102, 255)
    CYAN = (0, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

class GameCategory(Enum):
    """게임 카테고리"""
    SHOOTING = "🔫 슈팅"
    RACING = "🏎️ 레이싱"
    PUZZLE = "🧩 퍼즐"
    RPG = "🏰 RPG"
    SPORTS = "🥊 스포츠"
    BOARD = "♟️ 보드"

class GameInfo:
    """게임 정보"""
    def __init__(self, number, name, category, description=""):
        self.number = number
        self.name = name
        self.category = category
        self.description = description
        self.file = f"game_{number:03d}_{name.lower().replace(' ', '_')}_enhanced.py"

# 샘플 게임 목록 (6개 상세 구현 + 7개 기타)
GAMES = [
    # 슈팅 게임
    GameInfo(24, "Defender", GameCategory.SHOOTING, "클래식 방어 슈팅"),
    GameInfo(463, "Galaga", GameCategory.SHOOTING, "포메이션 기반 슈팅"),
    GameInfo(141, "Ikaruga", GameCategory.SHOOTING, "탄막 슈팅 게임"),
    
    # 레이싱 게임
    GameInfo(251, "Formula1", GameCategory.RACING, "고속 레이싱"),
    GameInfo(52, "OutRun", GameCategory.RACING, "열대 레이싱"),
    
    # 퍼즐 게임
    GameInfo(94, "Sokoban", GameCategory.PUZZLE, "박스 밀기 퍼즐"),
    GameInfo(96, "Sudoku", GameCategory.PUZZLE, "숫자 로직 퍼즐"),
    
    # RPG 게임
    GameInfo(103, "Dragon Quest", GameCategory.RPG, "클래식 RPG"),
    GameInfo(111, "Ultima", GameCategory.RPG, "고급 RPG"),
    
    # 스포츠 게임
    GameInfo(316, "Tekken", GameCategory.SPORTS, "격투 게임"),
    GameInfo(318, "Street Fighter", GameCategory.SPORTS, "한판 격투"),
    
    # 보드 게임
    GameInfo(77, "Monopoly", GameCategory.BOARD, "부동산 게임"),
    GameInfo(79, "Scrabble", GameCategory.BOARD, "단어 게임"),
]

class ArcadeLauncher:
    """아케이드 게임 런처"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 클래식 아케이드 게임 런처")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # 게임 상태
        self.running = True
        self.current_screen = "main_menu"  # main_menu, game_list, game_info
        self.selected_category = None
        self.selected_game = None
        self.highlighted_game = 0

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_screen == "game_list":
                        self.current_screen = "main_menu"
                    elif self.current_screen == "game_info":
                        self.current_screen = "game_list"
                    else:
                        self.running = False
                
                elif self.current_screen == "main_menu":
                    self._handle_main_menu_input(event.key)
                elif self.current_screen == "game_list":
                    self._handle_game_list_input(event.key)

    def _handle_main_menu_input(self, key):
        """메인 메뉴 입력"""
        if key == pygame.K_1:
            self.selected_category = GameCategory.SHOOTING
            self.current_screen = "game_list"
            self.highlighted_game = 0
        elif key == pygame.K_2:
            self.selected_category = GameCategory.RACING
            self.current_screen = "game_list"
            self.highlighted_game = 0
        elif key == pygame.K_3:
            self.selected_category = GameCategory.PUZZLE
            self.current_screen = "game_list"
            self.highlighted_game = 0
        elif key == pygame.K_4:
            self.selected_category = GameCategory.RPG
            self.current_screen = "game_list"
            self.highlighted_game = 0
        elif key == pygame.K_5:
            self.selected_category = GameCategory.SPORTS
            self.current_screen = "game_list"
            self.highlighted_game = 0
        elif key == pygame.K_6:
            self.selected_category = GameCategory.BOARD
            self.current_screen = "game_list"
            self.highlighted_game = 0

    def _handle_game_list_input(self, key):
        """게임 목록 입력"""
        category_games = [g for g in GAMES if g.category == self.selected_category]
        
        if key == pygame.K_UP:
            self.highlighted_game = max(0, self.highlighted_game - 1)
        elif key == pygame.K_DOWN:
            self.highlighted_game = min(len(category_games) - 1, self.highlighted_game + 1)
        elif key == pygame.K_RETURN:
            if 0 <= self.highlighted_game < len(category_games):
                self.selected_game = category_games[self.highlighted_game]
                self._launch_game(self.selected_game)

    def _launch_game(self, game):
        """게임 실행"""
        # game_NUMX_name_enhanced.py 또는 game_NUMX_name_detailed.py 파일 찾기
        base_name = f"game_{game.number:03d}_{game.name.lower().replace(' ', '_')}"

        # 상세 구현 버전 먼저 확인
        game_file = f"{base_name}_detailed.py"
        if not os.path.exists(game_file):
            # 강화 버전 확인
            game_file = f"{base_name}_enhanced.py"

        # 현재 디렉토리에서 파일 찾기
        if os.path.exists(game_file):
            subprocess.Popen([sys.executable, game_file])
        else:
            # 게임 파일 없으면 알림
            print(f"게임 파일을 찾을 수 없습니다: {base_name}_(detailed|enhanced).py")

    def draw_main_menu(self):
        """메인 메뉴 그리기"""
        self.screen.fill(Color.DARK_GRAY)

        # 타이틀
        title = self.font_large.render("🎮 클래식 아케이드 게임 런처", True, Color.CYAN)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - 280, 50))

        # 소제목
        subtitle = self.font_normal.render("카테고리를 선택하세요 (1-6)", True, Color.WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 150, 130))

        # 카테고리 목록
        categories = [
            ("1️⃣ 🔫 슈팅 게임 (3개)", 200),
            ("2️⃣ 🏎️ 레이싱 게임 (2개)", 270),
            ("3️⃣ 🧩 퍼즐 게임 (2개)", 340),
            ("4️⃣ 🏰 RPG 게임 (2개)", 410),
            ("5️⃣ 🥊 스포츠 게임 (2개)", 480),
            ("6️⃣ ♟️ 보드 게임 (2개)", 550),
        ]

        for cat_text, y in categories:
            text = self.font_normal.render(cat_text, True, Color.GREEN)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, y))

        # 하단 정보
        info = self.font_small.render("ESC: 종료", True, Color.GRAY)
        self.screen.blit(info, (50, SCREEN_HEIGHT - 50))

        stats = self.font_small.render(f"총 {len(GAMES)}개 게임 | 6개 상세 구현", True, Color.YELLOW)
        self.screen.blit(stats, (SCREEN_WIDTH - 350, SCREEN_HEIGHT - 50))

    def draw_game_list(self):
        """게임 목록 그리기"""
        self.screen.fill(Color.DARK_GRAY)

        # 타이틀
        category_name = self.selected_category.value
        title = self.font_large.render(f"{category_name} 게임", True, Color.CYAN)
        self.screen.blit(title, (50, 30))

        # 해당 카테고리 게임 목록
        category_games = [g for g in GAMES if g.category == self.selected_category]
        
        y_pos = 120
        for i, game in enumerate(category_games):
            if i == self.highlighted_game:
                # 선택된 게임
                bg_rect = pygame.Rect(40, y_pos - 5, SCREEN_WIDTH - 80, 50)
                pygame.draw.rect(self.screen, Color.BLUE, bg_rect)
                color = Color.YELLOW
                marker = "▶ "
            else:
                color = Color.WHITE
                marker = "  "

            game_text = f"{marker}[{game.number:03d}] {game.name}"
            text = self.font_normal.render(game_text, True, color)
            self.screen.blit(text, (50, y_pos))

            # 설명
            desc_text = self.font_small.render(game.description, True, Color.GRAY)
            self.screen.blit(desc_text, (100, y_pos + 30))

            y_pos += 80

        # 하단 정보
        info = self.font_small.render("↑/↓: 선택 | ENTER: 실행 | ESC: 뒤로", True, Color.GRAY)
        self.screen.blit(info, (50, SCREEN_HEIGHT - 50))

    def draw(self):
        """화면 그리기"""
        if self.current_screen == "main_menu":
            self.draw_main_menu()
        elif self.current_screen == "game_list":
            self.draw_game_list()

        pygame.display.flip()

    def run(self):
        """런처 실행"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    launcher = ArcadeLauncher()
    launcher.run()
