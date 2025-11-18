#!/usr/bin/env python3
"""
🧩 {game_name} (게임 {game_num})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from puzzle_game_template import PuzzleGame

class {game_name_title}Game(PuzzleGame):
    def __init__(self):
        super().__init__("{game_name_title}")
        # {game_name_title} 특화 설정 추가
        pass

    def _check_win(self):
        # 승리 조건 구현
        return False

if __name__ == "__main__":
    game = {game_name_title}Game()
    game.run()
