#!/usr/bin/env python3
"""
Chess - 상세 구현
턴 기반 전략 게임: 말을 이동하여 상대의 킹을 체크메이트
"""
import pygame
from enum import Enum
from graphics_themes import Color, Themes

class PieceType(Enum):
    """기물 종류"""
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6


class ChessPiece:
    """체스 기물"""

    def __init__(self, piece_type, is_white):
        self.type = piece_type
        self.is_white = is_white

    def get_symbol(self):
        """기물 기호"""
        symbols = {
            PieceType.PAWN: '♟' if self.is_white else '♙',
            PieceType.ROOK: '♜' if self.is_white else '♖',
            PieceType.KNIGHT: '♞' if self.is_white else '♘',
            PieceType.BISHOP: '♝' if self.is_white else '♗',
            PieceType.QUEEN: '♛' if self.is_white else '♕',
            PieceType.KING: '♚' if self.is_white else '♔'
        }
        return symbols.get(self.type, '?')

    def get_color(self):
        """기물 색상"""
        return Color.WHITE if self.is_white else Color.BLACK


class ChessGame:
    """Chess 상세 구현"""

    def __init__(self):
        pygame.init()

        self.window_width = 600
        self.window_height = 700
        self.game_name = "Chess"
        self.board_size = 8
        self.cell_size = 60

        # 게임 판
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self._setup_board()

        # 게임 상태
        self.selected_piece = None
        self.valid_moves = []
        self.white_turn = True
        self.game_over = False
        self.winner = None

        # 테마
        self.theme = Themes.LIGHT

        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.game_name)

        self.running = True

    def _setup_board(self):
        """보드 초기 설정"""
        # 검은 기물 (상단)
        back_row_black = [
            ChessPiece(PieceType.ROOK, False),
            ChessPiece(PieceType.KNIGHT, False),
            ChessPiece(PieceType.BISHOP, False),
            ChessPiece(PieceType.QUEEN, False),
            ChessPiece(PieceType.KING, False),
            ChessPiece(PieceType.BISHOP, False),
            ChessPiece(PieceType.KNIGHT, False),
            ChessPiece(PieceType.ROOK, False)
        ]
        self.board[0] = back_row_black

        # 검은 폰
        for x in range(self.board_size):
            self.board[1][x] = ChessPiece(PieceType.PAWN, False)

        # 흰 폰
        for x in range(self.board_size):
            self.board[6][x] = ChessPiece(PieceType.PAWN, True)

        # 흰 기물 (하단)
        back_row_white = [
            ChessPiece(PieceType.ROOK, True),
            ChessPiece(PieceType.KNIGHT, True),
            ChessPiece(PieceType.BISHOP, True),
            ChessPiece(PieceType.QUEEN, True),
            ChessPiece(PieceType.KING, True),
            ChessPiece(PieceType.BISHOP, True),
            ChessPiece(PieceType.KNIGHT, True),
            ChessPiece(PieceType.ROOK, True)
        ]
        self.board[7] = back_row_white

    def _get_valid_moves(self, x, y):
        """유효한 이동 목록"""
        piece = self.board[y][x]
        if not piece or piece.is_white != self.white_turn:
            return []

        moves = []

        if piece.type == PieceType.PAWN:
            direction = -1 if piece.is_white else 1
            # 앞으로 한 칸
            ny = y + direction
            if 0 <= ny < self.board_size and not self.board[ny][x]:
                moves.append((x, ny))

        elif piece.type == PieceType.ROOK:
            # 수평, 수직
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if not self.board[ny][nx]:
                        moves.append((nx, ny))
                    else:
                        if self.board[ny][nx].is_white != piece.is_white:
                            moves.append((nx, ny))
                        break
                    nx, ny = nx + dx, ny + dy

        elif piece.type == PieceType.KNIGHT:
            # L자 이동
            for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if not self.board[ny][nx] or self.board[ny][nx].is_white != piece.is_white:
                        moves.append((nx, ny))

        elif piece.type == PieceType.BISHOP:
            # 대각선
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if not self.board[ny][nx]:
                        moves.append((nx, ny))
                    else:
                        if self.board[ny][nx].is_white != piece.is_white:
                            moves.append((nx, ny))
                        break
                    nx, ny = nx + dx, ny + dy

        elif piece.type == PieceType.QUEEN:
            # 모든 방향
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                while 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if not self.board[ny][nx]:
                        moves.append((nx, ny))
                    else:
                        if self.board[ny][nx].is_white != piece.is_white:
                            moves.append((nx, ny))
                        break
                    nx, ny = nx + dx, ny + dy

        elif piece.type == PieceType.KING:
            # 한 칸 모든 방향
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        if not self.board[ny][nx] or self.board[ny][nx].is_white != piece.is_white:
                            moves.append((nx, ny))

        return moves

    def _handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 좌클릭
                    mouse_x, mouse_y = event.pos
                    board_x = mouse_x // self.cell_size
                    board_y = mouse_y // self.cell_size

                    if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
                        # 기물 선택 또는 이동
                        if (board_x, board_y) in self.valid_moves:
                            # 이동
                            sx, sy = self.selected_piece
                            self.board[board_y][board_x] = self.board[sy][sx]
                            self.board[sy][sx] = None
                            self.white_turn = not self.white_turn
                            self.selected_piece = None
                            self.valid_moves = []
                        else:
                            # 기물 선택
                            self.selected_piece = (board_x, board_y)
                            self.valid_moves = self._get_valid_moves(board_x, board_y)

    def _draw(self, surface):
        """화면 그리기"""
        surface.fill(Color.WHITE)

        # 체스 보드 그리기
        for y in range(self.board_size):
            for x in range(self.board_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                  self.cell_size, self.cell_size)

                # 체스판 색상
                if (x + y) % 2 == 0:
                    color = Color.WHITE
                else:
                    color = Color.LIGHT_GRAY

                pygame.draw.rect(surface, color, rect)

                # 유효한 이동 표시
                if (x, y) in self.valid_moves:
                    pygame.draw.circle(surface, Color.GREEN,
                                      (x * self.cell_size + self.cell_size // 2,
                                       y * self.cell_size + self.cell_size // 2), 5)

                # 선택된 기물 표시
                if self.selected_piece and self.selected_piece == (x, y):
                    pygame.draw.rect(surface, Color.YELLOW, rect, 3)

                pygame.draw.rect(surface, Color.BLACK, rect, 1)

        # 기물 그리기
        font = pygame.font.Font(None, 40)
        for y in range(self.board_size):
            for x in range(self.board_size):
                piece = self.board[y][x]
                if piece:
                    symbol_text = font.render(piece.get_symbol(), True, piece.get_color())
                    text_rect = symbol_text.get_rect(center=(x * self.cell_size + self.cell_size // 2,
                                                            y * self.cell_size + self.cell_size // 2))
                    surface.blit(symbol_text, text_rect)

        # 턴 표시
        font_small = pygame.font.Font(None, 24)
        turn_text = font_small.render(f"White's Turn" if self.white_turn else "Black's Turn",
                                     True, Color.BLACK)
        surface.blit(turn_text, (10, self.board_size * self.cell_size + 10))

    def run(self):
        """게임 실행"""
        while self.running:
            self._handle_input()
            self.clock.tick(60)
            self._draw(self.display)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()
