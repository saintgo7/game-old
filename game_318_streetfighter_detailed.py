#!/usr/bin/env python3
"""🥊 Street Fighter (게임 318) - 격투 게임"""
import pygame, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from sports_game_template import SportsGame, GameDifficulty
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class StreetFighterGame(SportsGame):
    """Street Fighter 게임"""
    def __init__(self):
        super().__init__("Street Fighter", difficulty=GameDifficulty.NORMAL)
        self.player.name = "Ryu"
        self.opponent.name = "Ken"

    def update(self):
        if self.paused or self.game_state.game_over:
            return

        if self.round_timer > 0:
            self.round_timer -= 1
        
        keys = pygame.key.get_pressed()
        self.handle_input(keys)
        
        self.player.update()
        self.ai.update(self.player)
        
        if self.round_timer <= 0 or self.player.hp <= 0 or self.opponent.hp <= 0:
            self._end_round()

    def draw(self):
        """그리기"""
        self.screen.fill(self.theme.bg_color)
        
        # 배경 (도장)
        pygame.draw.rect(self.screen, (139, 90, 43), (0, 250, SCREEN_WIDTH, 150))
        
        # 플레이어
        pygame.draw.rect(self.screen, Color.BLUE, (self.player.x, self.player.y, 40, 60))
        
        # 상대
        pygame.draw.rect(self.screen, Color.RED, (self.opponent.x, self.opponent.y, 40, 60))
        
        # 체력 바
        pygame.draw.rect(self.screen, Color.RED, (50, 20, 200, 20))
        pygame.draw.rect(self.screen, Color.GREEN, (50, 20, 200 * (self.player.hp / 100), 20))
        
        pygame.draw.rect(self.screen, Color.RED, (SCREEN_WIDTH - 250, 20, 200, 20))
        pygame.draw.rect(self.screen, Color.GREEN, (SCREEN_WIDTH - 250, 20, 200 * (self.opponent.hp / 100), 20))
        
        # UI
        round_text = self.font.render(f"Round {self.round_num}", True, Color.WHITE)
        self.screen.blit(round_text, (SCREEN_WIDTH // 2 - 60, 20))
        
        score_text = self.font.render(f"Score: {self.score}", True, Color.GREEN)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = StreetFighterGame()
    game.run()
