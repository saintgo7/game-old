#!/usr/bin/env python3
"""
🎮 Template Auto-Apply Script
All 024-500 games에 해당하는 게임 템플릿을 자동으로 적용하는 스크립트

게임을 분류하고 각 게임에 맞는 템플릿을 적용하여
자동으로 게임 파일 생성
"""

import os
import re
from pathlib import Path

# 게임 목록
GAMES_024_500 = {
    24: "defender", 25: "phoenix", 26: "digdug", 27: "bubblebobble",
    28: "bomberman", 29: "pacland", 30: "mspacman", 31: "ghouls",
    32: "joust", 33: "robotron", 34: "defender2", 35: "twinbee",
    36: "gradius", 37: "castlevania", 38: "megaman", 39: "kirby",
    40: "sonic", 41: "mariobros", 42: "supermario", 43: "dkjunior",
    44: "congo", 45: "qbert", 46: "digdug2", 47: "pengo",
    48: "rally", 49: "rallyx", 50: "bumpnjump", 51: "fformula",
    52: "outrun", 53: "sega", 54: "roadrunner", 55: "cruising",
    56: "poleposition", 57: "motorace", 58: "turf", 59: "tennis",
    60: "volleyball", 61: "basketball", 62: "baseball", 63: "football",
    64: "golf", 65: "boxing", 66: "bowling", 67: "poolshot",
    68: "darts", 69: "handball", 70: "pingpong", 71: "backgammon",
    72: "shogi", 73: "go", 74: "chinesecheck", 75: "ludo",
    76: "snakes", 77: "monopoly", 78: "risk", 79: "scrabble",
    80: "rummikub", 81: "jenga", 82: "Connect3D", 83: "Mastermind",
    84: "Battleship", 85: "Hangmanflex", 86: "Trivia", 87: "Quiz",
    88: "Wordgame", 89: "Textventure", 90: "Adventure", 91: "Dungeon",
    92: "MazeGame", 93: "Pushbox", 94: "Sokoban", 95: "Pipes",
    96: "Sudoku", 97: "Crossword", 98: "Jigsaw", 99: "Tangram",
    100: "Picross", 101: "Wizardry", 102: "Ultim", 103: "Dragon",
    104: "Rogue", 105: "Moria", 106: "Angband", 107: "Nethack",
    108: "DND", 109: "Final1", 110: "Dragon2", 111: "Ultima",
    112: "Exodus", 113: "Zork", 114: "Colossal", 115: "Enchant",
    116: "Scott", 117: "Infocom", 118: "Parser", 119: "Textadv",
    120: "Interact", 121: "Ys", 122: "Xanadu", 123: "Metroid",
    124: "IceClimber", 125: "Ghouls", 126: "CastleV2", 127: "Simon",
    128: "Belmont", 129: "BloodLines", 130: "Nocturne", 131: "Rondo",
    132: "Portrait", 133: "Symphony", 134: "Order", 135: "Curse",
    136: "Aria", 137: "PalOfLoan", 138: "SotnMode", 139: "IgaWare",
    140: "RomHacks", 141: "Ikaruga", 142: "Dodonpachi", 143: "Touhou",
    144: "Danmaku", 145: "Strikers", 146: "GalicaWar", 147: "Blazing",
    148: "Thunder", 149: "Raiden", 150: "Strikefly", 151: "Gungnir",
    152: "Hellfire", 153: "Gemini", 154: "Codename", 155: "Shmup",
    156: "VtolQst", 157: "Afterb", 158: "Xevious", 159: "Scrambl",
    160: "Sniping", 171: "Othello", 172: "Gomoku", 173: "MorabaraBAH",
    174: "Fanorona", 175: "Halma", 176: "Djambi", 177: "Hive",
    178: "Pandemic", 179: "Ticket", 180: "Carcass", 181: "TilePlace",
    182: "Agricola", 183: "Puerto", 184: "Onirim", 185: "Pandemic2",
    186: "Catan", 187: "Carcass2", 188: "PuertoR2", 189: "Agricol2",
    190: "TTRails", 201: "DDR", 202: "ITGCustom", 203: "StepMania",
    204: "OpenDDR", 205: "BeatSaber", 206: "RhythmGame", 207: "Taiko",
    208: "PopsMN", 209: "ParaPara", 210: "Bemani", 211: "Gitaroo",
    212: "GuitarFX", 213: "RockBand", 214: "GuitarHero", 215: "AudioSrf",
    216: "MusicRhy", 217: "Melodia", 218: "Harmonic", 219: "Synthesia",
    220: "NotePiano", 251: "F1Race", 252: "F1Pole", 253: "TouringC",
    254: "IndyCar", 255: "NHRA", 256: "Rally", 257: "Sega",
    258: "MarioKart", 259: "CrashTeam", 260: "WildTeam", 261: "Diddy",
    262: "ModNation", 263: "TrackMania", 264: "FlatOut", 265: "Burnout",
    266: "NeedSpeed", 267: "GTA", 268: "CannonFd", 269: "HotWheels",
    270: "MicroMach", 301: "SnMWars", 302: "WolfStein", 303: "Doom",
    304: "Heretic", 305: "Hexen", 306: "Strife", 307: "Chasm",
    308: "DukeNuke", 309: "Blood", 310: "Shadow", 311: "PowerSlave",
    312: "Build", 313: "Rage", 314: "Blackcrypt", 315: "CyClones",
    316: "Tekken", 317: "Mortal", 318: "SF", 319: "StreetFght",
    320: "FighterChamp", 351: "AdvanceWars", 352: "FireEmblem", 353: "TacticsOgre",
    354: "FFT", 355: "Disgaea", 356: "Vandal", 357: "Dynasty",
    358: "Samurai", 359: "Koei", 360: "Total", 361: "StarCraft",
    362: "Warcraft", 363: "Dune", 364: "Civilization", 365: "Master",
    366: "XCom", 367: "TheGame", 368: "FallOut", 369: "EldoRado",
    370: "Baldur", 401: "SimCity", 402: "SimTower", 403: "SimFarm",
    404: "SimEarth", 405: "Tycoon", 406: "RolerCoast", 407: "Hospital",
    408: "Theme", 409: "Tropico", 410: "Banished", 411: "TwoPoint",
    412: "OpenTTD", 413: "VintageStory", 414: "Minecraft", 415: "Terraria",
    416: "Stardew", 417: "Animal", 418: "Harvest", 419: "Story",
    420: "CastleVillain", 451: "PacManWorld", 452: "DiddyRacing", 453: "StarFox",
    454: "F-Zero", 455: "Waverace", 456: "Seaquest", 457: "Atlantis",
    458: "AnalogGame", 459: "Breakout2", 460: "ArkanoidII", 461: "ArkanoidIII",
    462: "Darius", 463: "GalagaII", 464: "GalagaIII", 465: "Gator",
    466: "Kicker", 467: "Lumber", 468: "Super", 469: "Spy",
    470: "Unknown", 471: "ThePitII", 472: "ThePitIII", 473: "Kaboom",
    474: "Centiped2", 475: "Millipede", 476: "Vortex", 477: "Pengo2",
    478: "Track", 479: "Mousetrap", 480: "Kangaroo", 481: "Kingkong",
    482: "Elevator", 483: "LordCastle", 484: "MonsterMaze", 485: "DeathRace",
    486: "HighScore", 487: "LaserBase", 488: "Stargate", 489: "Radar",
    490: "UFO", 491: "CloneGame", 492: "Pengo3", 493: "ArcadeAce",
    494: "GameOver", 495: "VectorGame", 496: "3DVektor", 497: "ArcadeCustom",
    498: "RetroVibe", 499: "ClassicMode", 500: "MasterArcade"
}

def categorize_game(game_num, game_name):
    """게임을 카테고리로 분류"""
    name_lower = game_name.lower()

    # 슈팅 게임
    shooting_keywords = ["defender", "phoenix", "gradius", "twinbee", "ikaruga", "dodonpachi",
                        "touhou", "danmaku", "raiden", "xevious", "galaga", "shmup",
                        "strikers", "blazing", "thunder", "strikefly", "gungnir", "hellfire"]
    if any(kw in name_lower for kw in shooting_keywords):
        return "shooting"

    # 레이싱 게임
    racing_keywords = ["rally", "outrun", "sega", "motorace", "poleposition", "f1", "formula",
                       "indy", "nhra", "mario", "kart", "crash", "wild", "diddy", "modnation",
                       "track", "flatout", "burnout", "needspeed", "gta", "cannon", "hot wheels",
                       "micro", "zero", "wave", "race", "touring"]
    if any(kw in name_lower for kw in racing_keywords):
        return "racing"

    # 퍼즐 게임
    puzzle_keywords = ["sokoban", "sudoku", "picross", "tetris", "crossword", "jigsaw",
                       "tangram", "pipes", "maze", "pushbox", "q-bert", "arkanoid",
                       "breakout", "darius"]
    if any(kw in name_lower for kw in puzzle_keywords):
        return "puzzle"

    # RPG 게임
    rpg_keywords = ["wizard", "rogue", "moria", "angband", "nethack", "dnd", "final", "dragon",
                    "ultima", "exodus", "zork", "colossal", "enchant", "scott", "infocom",
                    "ys", "xanadu", "metroid", "ice climber", "belmont", "blood", "nocturne",
                    "rondo", "portrait", "symphony", "aria", "tacticsogre", "fft", "disgaea",
                    "dynasty", "samurai", "total", "starcraft", "warcraft", "dune", "civilization",
                    "fallout", "baldur", "onirim", "pandemic", "agricola", "puerto"]
    if any(kw in name_lower for kw in rpg_keywords):
        return "rpg"

    # 보드/카드 게임
    board_keywords = ["othello", "gomoku", "monopoly", "risk", "scrabble", "rummikub", "jenga",
                      "mastermind", "battleship", "hangman", "trivia", "quiz", "backgammon",
                      "shogi", "go", "ludo", "snakes", "fanorona", "halma", "djambi", "hive",
                      "ticket", "carcass", "catan", "rails"]
    if any(kw in name_lower for kw in board_keywords):
        return "board"

    # 스포츠/격투 게임
    sports_keywords = ["tekken", "mortal", "street", "fighter", "boxing", "bowling", "tennis",
                       "volleyball", "basketball", "baseball", "football", "golf", "darts",
                       "handball", "pingpong", "poolshot", "kicker"]
    if any(kw in name_lower for kw in sports_keywords):
        return "sports"

    # 액션/어드벤처
    action_keywords = ["castlevania", "megaman", "kirby", "sonic", "mario", "donkey",
                       "ghouls", "ghost", "joust", "robotron", "digdug", "pacman",
                       "bubble", "bomberman", "congo", "qbert", "pengo"]
    if any(kw in name_lower for kw in action_keywords):
        return "shooting"  # 기본값으로 슈팅으로 분류

    # 리듬 게임
    rhythm_keywords = ["ddr", "beat", "rhythm", "taiko", "para", "bemani", "guitar",
                       "rock", "guitar hero", "audio", "music"]
    if any(kw in name_lower for kw in rhythm_keywords):
        return "puzzle"  # 리듬을 퍼즐처럼 취급

    # 건설/시뮬레이션
    sim_keywords = ["sim", "tycoon", "roller", "hospital", "theme", "tropico", "banished",
                    "openttd", "vintage", "minecraft", "terraria", "stardew", "animal",
                    "harvest"]
    if any(kw in name_lower for kw in sim_keywords):
        return "puzzle"  # 구성 게임을 퍼즐처럼 취급

    # 전술 게임
    tactical_keywords = ["advance", "fire", "emblem", "tacticsogre"]
    if any(kw in name_lower for kw in tactical_keywords):
        return "rpg"

    # 기본값 (분류 안 됨)
    return "shooting"

def generate_template_code(game_num, game_name, category):
    """게임 템플릿 코드 생성"""
    name_title = game_name.title()
    name_slug = game_name.lower().replace(" ", "_").replace("-", "_")

    code_templates = {
        "shooting": f'''#!/usr/bin/env python3
"""
🔫 {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from shooting_game_template import ShootingGame, GameDifficulty

class {{game_name_title}}Game(ShootingGame):
    def __init__(self):
        super().__init__("{{game_name_title}}", difficulty=GameDifficulty.NORMAL)
        # {{game_name_title}} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
''',
        "racing": f'''#!/usr/bin/env python3
"""
🏎️ {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from racing_game_template import RacingGame

class {{game_name_title}}Game(RacingGame):
    def __init__(self):
        super().__init__("{{game_name_title}}")
        # {{game_name_title}} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
''',
        "puzzle": f'''#!/usr/bin/env python3
"""
🧩 {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from puzzle_game_template import PuzzleGame

class {{game_name_title}}Game(PuzzleGame):
    def __init__(self):
        super().__init__("{{game_name_title}}")
        # {{game_name_title}} 특화 설정 추가
        pass

    def _check_win(self):
        # 승리 조건 구현
        return False

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
''',
        "rpg": f'''#!/usr/bin/env python3
"""
🏰 {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from rpg_game_template import RPGGame

class {{game_name_title}}Game(RPGGame):
    def __init__(self):
        super().__init__("{{game_name_title}}")
        # {{game_name_title}} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
''',
        "sports": f'''#!/usr/bin/env python3
"""
🥊 {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from sports_game_template import SportsGame, GameDifficulty

class {{game_name_title}}Game(SportsGame):
    def __init__(self):
        super().__init__("{{game_name_title}}", difficulty=GameDifficulty.NORMAL)
        # {{game_name_title}} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
''',
        "board": f'''#!/usr/bin/env python3
"""
♟️ {{game_name}} (게임 {{game_num}})
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from board_game_template import BoardGame, GameDifficulty

class {{game_name_title}}Game(BoardGame):
    def __init__(self):
        super().__init__("{{game_name_title}}", difficulty=GameDifficulty.NORMAL)
        # {{game_name_title}} 특화 설정 추가
        pass

if __name__ == "__main__":
    game = {{game_name_title}}Game()
    game.run()
'''
    }

    template = code_templates.get(category, code_templates["shooting"])
    code = template.replace("{{game_name}}", game_name)
    code = code.replace("{{game_num}}", str(game_num))
    code = code.replace("{{game_name_title}}", name_title)
    code = code.replace("{{game_name_slug}}", name_slug)

    return code

def main():
    """메인 함수"""
    print("🎮 게임 템플릿 자동 적용 시작...")
    print(f"총 {len(GAMES_024_500)}개 게임 처리 중...")

    # 통계
    stats = {
        "shooting": 0, "racing": 0, "puzzle": 0,
        "rpg": 0, "sports": 0, "board": 0
    }

    for game_num in sorted(GAMES_024_500.keys()):
        game_name = GAMES_024_500[game_num]
        category = categorize_game(game_num, game_name)
        stats[category] += 1

        # 게임 파일명
        filename = f"game_{game_num:03d}_{game_name}.py"

        # 이미 있으면 생략 (샘플 게임 보존)
        if os.path.exists(filename):
            print(f"  ⏭️  {game_num:3d}: {game_name:20s} [{category:10s}] - 이미 존재")
            continue

        # 템플릿 코드 생성
        code = generate_template_code(game_num, game_name, category)

        # 파일 저장
        try:
            with open(filename, 'w') as f:
                f.write(code)
            print(f"  ✅ {game_num:3d}: {game_name:20s} [{category:10s}] - 생성됨")
        except Exception as e:
            print(f"  ❌ {game_num:3d}: {game_name:20s} - 오류: {e}")

    # 통계 출력
    print("\n📊 분류 통계:")
    print(f"  🔫 슈팅: {stats['shooting']:3d}개")
    print(f"  🏎️ 레이싱: {stats['racing']:3d}개")
    print(f"  🧩 퍼즐: {stats['puzzle']:3d}개")
    print(f"  🏰 RPG: {stats['rpg']:3d}개")
    print(f"  🥊 스포츠: {stats['sports']:3d}개")
    print(f"  ♟️ 보드: {stats['board']:3d}개")
    print(f"  합계: {sum(stats.values())}개")

if __name__ == "__main__":
    main()
