#!/usr/bin/env python3
"""
♟️ 보드/카드 게임 템플릿
Monopoly, Scrabble, Chess, Go, Shogi, Othello, Backgammon 등 턴 기반 게임의 기본 구현
"""

import pygame
import random
import sys
from pathlib import Path
from enum import Enum
from collections import deque

sys.path.insert(0, str(Path(__file__).parent.parent))

from game_utils import ScoreManager, GameConfig, GameState
from sound_manager import SoundManager
from graphics_themes import Themes, Color

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
FPS = 60

class GameDifficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXTREME = 4

class GamePiece:
    """게임 말/기물"""
    def __init__(self, x, y, piece_type, player_id, size=30):
        self.x = x
        self.y = y
        self.piece_type = piece_type
        self.player_id = player_id  # 0: 플레이어, 1: AI
        self.size = size
        self.selected = False
        self.valid_moves = []

    def draw(self, surface, color):
        """그리기"""
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)
        if self.selected:
            pygame.draw.circle(surface, Color.YELLOW, (self.x, self.y), self.size + 3, 3)

class BoardTile:
    """보드 타일"""
    def __init__(self, x, y, tile_id, width=40, height=40):
        self.x = x
        self.y = y
        self.tile_id = tile_id
        self.width = width
        self.height = height
        self.piece = None
        self.type = "normal"  # normal, special, trap, bonus
        self.owner = None  # 소유자 (보드게임 경우)

    def contains_point(self, px, py):
        """점이 타일 내부인지 확인"""
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)

    def draw(self, surface, theme):
        """그리기"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 타입별 색상
        if self.type == "special":
            color = Color.CYAN
        elif self.type == "trap":
            color = Color.RED
        elif self.type == "bonus":
            color = Color.GREEN
        else:
            color = self.theme.secondary_color if hasattr(self, 'theme') else Color.WHITE

        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, Color.GRAY, rect, 1)

        # 소유자 표시
        if self.owner is not None:
            owner_color = Color.BLUE if self.owner == 0 else Color.RED
            pygame.draw.rect(surface, owner_color, rect, 3)

class GameRule:
    """게임 규칙 엔진"""
    def __init__(self, rule_type="standard"):
        self.rule_type = rule_type
        self.board_size = 8  # 기본 8x8
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.valid_moves_cache = {}

    def get_valid_moves(self, piece, board_state=None):
        """유효한 이동 가능 위치 반환 (오버라이드 필요)"""
        moves = []
        # 기본: 인접한 4방향
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        x, y = piece.x // 40, piece.y // 40  # 보드 좌표로 변환

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                moves.append((nx * 40, ny * 40))

        return moves

    def is_valid_move(self, piece, target_x, target_y):
        """이동이 유효한지 확인"""
        valid_moves = self.get_valid_moves(piece)
        return (target_x, target_y) in valid_moves

    def check_win_condition(self, player_score, opponent_score, turn_count):
        """승리 조건 확인"""
        if turn_count >= 100:  # 100턴 후 점수로 판정
            return player_score > opponent_score
        return False

class AIPlayer:
    """AI 플레이어"""
    def __init__(self, difficulty=GameDifficulty.NORMAL):
        self.difficulty = difficulty
        self.decision_timer = 0
        self.decision_interval = 30
        self.current_move = None

    def make_move(self, board_state, player_pieces, opponent_pieces):
        """이동 결정"""
        if self.difficulty == GameDifficulty.EASY:
            return self._easy_move(player_pieces)
        elif self.difficulty == GameDifficulty.NORMAL:
            return self._normal_move(player_pieces, opponent_pieces)
        elif self.difficulty == GameDifficulty.HARD:
            return self._hard_move(player_pieces, opponent_pieces)
        else:  # EXTREME
            return self._extreme_move(player_pieces, opponent_pieces)

    def _easy_move(self, pieces):
        """쉬움: 랜덤 이동"""
        if pieces:
            piece = random.choice(pieces)
            return piece, random.choice(piece.valid_moves) if piece.valid_moves else None
        return None, None

    def _normal_move(self, player_pieces, opponent_pieces):
        """보통: 전략적 선택"""
        best_piece = None
        best_move = None
        best_score = -float('inf')

        for piece in player_pieces:
            for move in piece.valid_moves[:3]:  # 처음 3개만 평가
                score = random.randint(0, 100)
                if score > best_score:
                    best_score = score
                    best_piece = piece
                    best_move = move

        return best_piece, best_move

    def _hard_move(self, player_pieces, opponent_pieces):
        """어려움: 공격 우선"""
        # 상대 기물 공격 가능한 이동 찾기
        for piece in player_pieces:
            for move in piece.valid_moves:
                for opp in opponent_pieces:
                    if abs(move[0] - opp.x) < 50 and abs(move[1] - opp.y) < 50:
                        return piece, move

        # 없으면 일반 이동
        return self._normal_move(player_pieces, opponent_pieces)

    def _extreme_move(self, player_pieces, opponent_pieces):
        """매우 어려움: 최적 전략"""
        # 상대 기물 공격 + 방어 고려
        defensive_moves = []
        offensive_moves = []

        for piece in player_pieces:
            for move in piece.valid_moves:
                for opp in opponent_pieces:
                    if abs(move[0] - opp.x) < 50 and abs(move[1] - opp.y) < 50:
                        offensive_moves.append((piece, move))

        # 공격 이동이 있으면 선택, 없으면 방어 이동
        if offensive_moves:
            piece, move = random.choice(offensive_moves)
            return piece, move

        return self._normal_move(player_pieces, opponent_pieces)

class BoardGame:
    """보드/카드 게임 기본 클래스"""
    def __init__(self, game_name, difficulty=GameDifficulty.NORMAL):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"♟️ {game_name}")
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

        # 보드와 규칙
        self.board_size = 8
        self.tile_width = 40
        self.tile_height = 40
        self.board_start_x = 50
        self.board_start_y = 100

        self.tiles = self._create_board()
        self.game_rules = GameRule()

        # 게임 오브젝트
        self.player_pieces = []
        self.ai_pieces = []
        self.selected_piece = None

        # 턴 관리
        self.current_turn = 0  # 0: 플레이어, 1: AI
        self.turn_timer = 180  # 3초
        self.turn_count = 0
        self.max_turns = 100

        # 점수
        self.player_score = 0
        self.ai_score = 0
        self.move_history = deque(maxlen=20)

        # AI
        self.ai_player = AIPlayer(difficulty)

        # 초기 피스 배치
        self._setup_pieces()

    def _create_board(self):
        """보드 생성"""
        tiles = []
        for y in range(self.board_size):
            row = []
            for x in range(self.board_size):
                tile = BoardTile(
                    self.board_start_x + x * self.tile_width,
                    self.board_start_y + y * self.tile_height,
                    y * self.board_size + x
                )
                # 특수 타일 (체스판 패턴)
                if (x + y) % 2 == 0:
                    tile.type = "normal"
                else:
                    tile.type = "normal"

                row.append(tile)
            tiles.append(row)

        return tiles

    def _setup_pieces(self):
        """초기 피스 배치"""
        # 플레이어 피스 (아래쪽)
        for i in range(3):
            piece = GamePiece(
                self.board_start_x + i * self.tile_width + self.tile_width // 2,
                self.board_start_y + (self.board_size - 1) * self.tile_height + self.tile_height // 2,
                "normal",
                0
            )
            self.player_pieces.append(piece)

        # AI 피스 (위쪽)
        for i in range(3):
            piece = GamePiece(
                self.board_start_x + i * self.tile_width + self.tile_width // 2,
                self.board_start_y + self.tile_height // 2,
                "normal",
                1
            )
            self.ai_pieces.append(piece)

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
                elif event.key == pygame.K_u:
                    self._undo_move()
                elif event.key == pygame.K_SPACE:
                    self._new_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)

    def _handle_click(self, pos):
        """마우스 클릭 처리"""
        if self.current_turn != 0:  # AI 턴이면 무시
            return

        # 보드 타일 클릭
        for row in self.tiles:
            for tile in row:
                if tile.contains_point(pos[0], pos[1]):
                    self._handle_tile_click(tile, pos)
                    return

        # 피스 클릭
        for piece in self.player_pieces:
            dist = ((piece.x - pos[0])**2 + (piece.y - pos[1])**2)**0.5
            if dist < piece.size + 10:
                self._select_piece(piece)
                return

    def _handle_tile_click(self, tile, pos):
        """타일 클릭 처리"""
        if self.selected_piece:
            # 유효한 이동이면 이동
            if self.game_rules.is_valid_move(self.selected_piece, tile.x, tile.y):
                old_pos = (self.selected_piece.x, self.selected_piece.y)
                self.selected_piece.x = tile.x + self.tile_width // 2
                self.selected_piece.y = tile.y + self.tile_height // 2
                self.move_history.append((self.selected_piece, old_pos))
                self.selected_piece = None
                self.player_score += 10
                self._end_turn()

    def _select_piece(self, piece):
        """피스 선택"""
        # 이전 선택 해제
        if self.selected_piece:
            self.selected_piece.selected = False

        # 새로운 선택
        piece.selected = True
        piece.valid_moves = self.game_rules.get_valid_moves(piece)
        self.selected_piece = piece

    def _end_turn(self):
        """턴 종료"""
        self.current_turn = 1  # AI 턴으로
        self.turn_timer = 120

    def _undo_move(self):
        """이동 취소"""
        if self.move_history and self.current_turn == 0:
            piece, old_pos = self.move_history.pop()
            piece.x, piece.y = old_pos
            self.player_score = max(0, self.player_score - 10)

    def _new_game(self):
        """새 게임"""
        self.player_pieces.clear()
        self.ai_pieces.clear()
        self._setup_pieces()
        self.turn_count = 0
        self.player_score = 0
        self.ai_score = 0
        self.current_turn = 0
        self.game_state.game_over = False
        self.move_history.clear()

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return

        self.turn_count += 1
        self.turn_timer -= 1

        # AI 턴
        if self.current_turn == 1:
            if self.turn_timer <= 0:
                piece, move = self.ai_player.make_move(
                    self.tiles,
                    self.ai_pieces,
                    self.player_pieces
                )

                if piece and move:
                    piece.x = move[0] + self.tile_width // 2
                    piece.y = move[1] + self.tile_height // 2
                    self.ai_score += 10

                self.current_turn = 0
                self.turn_timer = 180

        # 승리 조건 확인
        if self.game_rules.check_win_condition(
            self.player_score,
            self.ai_score,
            self.turn_count
        ):
            self.game_state.game_over = True

        if self.turn_count >= self.max_turns:
            self.game_state.game_over = True

    def draw(self):
        """화면 그리기"""
        self.screen.fill(self.theme.bg_color)

        # 보드 그리기
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen, self.theme)

        # 피스 그리기
        for piece in self.player_pieces:
            piece.draw(self.screen, Color.BLUE)

        for piece in self.ai_pieces:
            piece.draw(self.screen, Color.RED)

        # UI 정보
        ui_x = self.board_start_x + self.board_size * self.tile_width + 50

        # 제목
        title_text = self.font.render("Board Game", True, self.theme.text_color)
        self.screen.blit(title_text, (ui_x, 100))

        # 턴 정보
        turn_text = self.small_font.render(
            f"Turn: {self.turn_count}/{self.max_turns}",
            True,
            self.theme.text_color
        )
        self.screen.blit(turn_text, (ui_x, 150))

        current_player = "Player" if self.current_turn == 0 else "AI"
        player_text = self.small_font.render(
            f"Current: {current_player}",
            True,
            Color.BLUE if self.current_turn == 0 else Color.RED
        )
        self.screen.blit(player_text, (ui_x, 180))

        # 점수
        score_title = self.font.render("Score", True, self.theme.text_color)
        self.screen.blit(score_title, (ui_x, 220))

        player_score_text = self.small_font.render(
            f"Player: {self.player_score}",
            True,
            Color.BLUE
        )
        self.screen.blit(player_score_text, (ui_x, 260))

        ai_score_text = self.small_font.render(
            f"AI: {self.ai_score}",
            True,
            Color.RED
        )
        self.screen.blit(ai_score_text, (ui_x, 290))

        # 컨트롤 정보
        controls = [
            "Click: Select/Move",
            "U: Undo",
            "P: Pause",
            "SPACE: New Game",
            "ESC: Exit"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, self.theme.text_color)
            self.screen.blit(control_text, (ui_x, 350 + i * 30))

        # 일시정지
        if self.paused:
            pause_text = self.font.render("PAUSED", True, Color.RED)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # 게임 오버
        if self.game_state.game_over:
            winner = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!" if self.ai_score > self.player_score else "Draw!"
            winner_color = Color.BLUE if self.player_score > self.ai_score else Color.RED if self.ai_score > self.player_score else Color.YELLOW

            over_text = self.font.render(winner, True, winner_color)
            self.screen.blit(over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

            final_text = self.small_font.render(
                f"Player: {self.player_score} vs AI: {self.ai_score}",
                True,
                self.theme.text_color
            )
            self.screen.blit(final_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        """게임 실행"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        # 점수 저장
        if self.player_score > 0:
            rank = self.score_manager.add_score(
                self.config.get("player_name", "Player"),
                self.player_score
            )

        pygame.quit()
