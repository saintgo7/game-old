#!/usr/bin/env python3
"""
🏰 {game_name} (게임 {game_num})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from rpg_game_template import RPGGame

class {game_name_title}Game(RPGGame):
    def __init__(self):
        super().__init__("{game_name_title}")
        # {game_name_title} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {game_name_title}Game()
    game.run()
