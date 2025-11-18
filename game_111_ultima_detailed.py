#!/usr/bin/env python3
"""🏰 Ultima (게임 111) - 고급 RPG"""
import pygame, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from rpg_game_template import RPGGame, Player, NPC, Enemy
from graphics_themes import Color

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class UltimaGame(RPGGame):
    """Ultima 게임"""
    def __init__(self):
        super().__init__("Ultima")
        self.shops = {
            "sword": {"price": 100, "attack": 10},
            "shield": {"price": 80, "defense": 5},
            "potion": {"price": 20, "heal": 50}
        }
        self.inventory = {}
        self.quest_target = None

    def update(self):
        if self.paused or self.game_state.game_over:
            return
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= 2
        if keys[pygame.K_RIGHT]:
            self.player.x += 2
        if keys[pygame.K_UP]:
            self.player.y -= 2
        if keys[pygame.K_DOWN]:
            self.player.y += 2
        
        self.player.x = max(0, min(SCREEN_WIDTH - 20, self.player.x))
        self.player.y = max(0, min(SCREEN_HEIGHT - 20, self.player.y))
        
        # 무작위 적 만남
        if random.random() < 0.001:
            self.in_battle = True
            enemy_names = ["Demon", "Dragon", "Skeleton"]
            self.current_enemy = Enemy(0, 0, random.choice(enemy_names), 50, 10)
            self.score += 100

    def draw(self):
        """그리기"""
        self.screen.fill(self.theme.bg_color)
        
        # 플레이어
        pygame.draw.circle(self.screen, Color.BLUE, (int(self.player.x), int(self.player.y)), 10)
        
        # NPC
        for npc in self.npcs:
            pygame.draw.circle(self.screen, Color.GREEN, (int(npc.x), int(npc.y)), 8)
        
        # 적 (배틀 중)
        if self.in_battle and self.current_enemy:
            pygame.draw.circle(self.screen, Color.RED, (400, 300), 15)
        
        # UI
        stats = [
            f"Level: {self.player.level}",
            f"HP: {self.player.hp}/{self.player.max_hp}",
            f"Gold: {self.player.gold}",
            f"Score: {self.score}"
        ]
        for i, stat in enumerate(stats):
            text = self.small_font.render(stat, True, Color.WHITE)
            self.screen.blit(text, (10, 10 + i * 25))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = UltimaGame()
    game.run()
