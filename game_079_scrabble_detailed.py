#!/usr/bin/env python3
"""♟️ Scrabble (게임 079) - 단어 게임"""
import pygame, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from board_game_template import BoardGame, GameDifficulty
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

class ScrabbleGame(BoardGame):
    """Scrabble 게임"""
    def __init__(self):
        super().__init__("Scrabble", difficulty=GameDifficulty.NORMAL)
        self.board_size = 15
        self.tiles = self._create_board()
        self.letter_values = {chr(i): i - 64 for i in range(65, 91)}
        self.words_played = []

    def _create_board(self):
        """보드 생성"""
        tiles = []
        for y in range(self.board_size):
            row = []
            for x in range(self.board_size):
                from board_game_template import BoardTile
                tile = BoardTile(100 + x * 40, 150 + y * 40, y * self.board_size + x, 40, 40)
                row.append(tile)
            tiles.append(row)
        return tiles

    def update(self):
        """게임 업데이트"""
        if self.paused or self.game_state.game_over:
            return
        
        self.turn_count += 1
        if self.turn_count >= self.max_turns:
            self.game_state.game_over = True

    def draw(self):
        """그리기"""
        self.screen.fill(self.theme.bg_color)
        
        # 보드 그리기 (15x15)
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(self.screen, Color.YELLOW, (tile.x, tile.y, 40, 40))
                pygame.draw.rect(self.screen, Color.BLACK, (tile.x, tile.y, 40, 40), 1)
        
        # 점수 표시
        score_text = self.font.render(f"Player: {self.player_score}", True, Color.BLUE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 250, 50))
        
        ai_score_text = self.font.render(f"AI: {self.ai_score}", True, Color.RED)
        self.screen.blit(ai_score_text, (SCREEN_WIDTH - 250, 100))
        
        turn_text = self.small_font.render(f"Turn: {self.turn_count}", True, Color.WHITE)
        self.screen.blit(turn_text, (SCREEN_WIDTH - 250, 150))
        
        if self.game_state.game_over:
            over = self.font.render("GAME OVER", True, Color.GREEN)
            self.screen.blit(over, (SCREEN_WIDTH // 2 - 100, 50))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = ScrabbleGame()
    game.run()
