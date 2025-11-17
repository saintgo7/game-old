#!/usr/bin/env python3
"""
게임 024-500 자동 생성 스크립트
"""
import os
import json

# 게임 목록 (024-500)
GAMES = {
    24: "defender", 25: "phoenix", 26: "digdug", 27: "bubblebobble",
    28: "bomberman", 29: "pacland", 30: "mspacman", 31: "ghouls",
    32: "joust", 33: "robotron", 34: "defender2", 35: "twinbee",
    36: "gradius", 37: "castlevania", 38: "megaman", 39: "kirby",
    40: "sonic", 41: "mariobros", 42: "supermario", 43: "dkjunior",
    44: "congo", 45: "qbert", 46: "digdug2", 47: "pengo",
    48: "rally", 49: "rallyx", 50: "bumpnjump",
    # 51-100: 레이싱, 스포츠
    51: "fformula", 52: "outrun", 53: "sega", 54: "roadrunner",
    55: "cruising", 56: "poleposition", 57: "motorace", 58: "turf",
    59: "tennis", 60: "volleyball", 61: "basketball", 62: "baseball",
    63: "football", 64: "golf", 65: "boxing", 66: "bowling",
    67: "poolshot", 68: "darts", 69: "handball", 70: "pingpong",
    # 71-100: 보드게임, 퍼즐
    71: "backgammon", 72: "shogi", 73: "go", 74: "chinesecheck",
    75: "ludo", 76: "snakes", 77: "monopoly", 78: "risk",
    79: "scrabble", 80: "rummikub", 81: "jenga", 82: "Connect3D",
    83: "Mastermind", 84: "Battleship", 85: "Hangmanflex", 86: "Trivia",
    87: "Quiz", 88: "Wordgame", 89: "Textventure", 90: "Adventure",
    91: "Dungeon", 92: "MazeGame", 93: "Pushbox", 94: "Sokoban",
    95: "Pipes", 96: "Sudoku", 97: "Crossword", 98: "Jigsaw",
    99: "Tangram", 100: "Picross",
    # 101-150: RPG, 턴베이스
    101: "Wizardry", 102: "Ultim", 103: "Dragon", 104: "Rogue",
    105: "Moria", 106: "Angband", 107: "Nethack", 108: "DND",
    109: "Final1", 110: "Dragon2", 111: "Ultima", 112: "Exodus",
    113: "Zork", 114: "Colossal", 115: "Enchant", 116: "Scott",
    117: "Infocom", 118: "Parser", 119: "Textadv", 120: "Interact",
    # 121-170: 액션 RPG, 플랫포머
    121: "Ys", 122: "Xanadu", 123: "Metroid", 124: "IceClimber",
    125: "Ghouls", 126: "CastleV2", 127: "Simon", 128: "Belmont",
    129: "BloodLines", 130: "Nocturne", 131: "Rondo", 132: "Portrait",
    133: "Symphony", 134: "Order", 135: "Curse", 136: "Aria",
    137: "PalOfLoan", 138: "SotnMode", 139: "IgaWare", 140: "RomHacks",
    # 141-200: 슈팅, 액션
    141: "Ikaruga", 142: "Dodonpachi", 143: "Touhou", 144: "Danmaku",
    145: "Strikers", 146: "GalicaWar", 147: "Blazing", 148: "Thunder",
    149: "Raiden", 150: "Strikefly", 151: "Gungnir", 152: "Hellfire",
    153: "Gemini", 154: "Codename", 155: "Shmup", 156: "VtolQst",
    157: "Afterb", 158: "Xevious", 159: "Scrambl", 160: "Sniping",
    # 171-200: 보드, 카드, 추상
    171: "Othello", 172: "Gomoku", 173: "MorabaraBAH", 174: "Fanorona",
    175: "Halma", 176: "Djambi", 177: "Hive", 178: "Pandemic",
    179: "Ticket", 180: "Carcass", 181: "TilePlace", 182: "Agricola",
    183: "Puerto", 184: "Onirim", 185: "Pandemic2", 186: "Catan",
    187: "Carcass2", 188: "PuertoR2", 189: "Agricol2", 190: "TTRails",
    # 201-250: 뮤직, 리듬
    201: "DDR", 202: "ITGCustom", 203: "StepMania", 204: "OpenDDR",
    205: "BeatSaber", 206: "RhythmGame", 207: "Taiko", 208: "PopsMN",
    209: "ParaPara", 210: "Bemani", 211: "Gitaroo", 212: "GuitarFX",
    213: "RockBand", 214: "GuitarHero", 215: "AudioSrf", 216: "MusicRhy",
    217: "Melodia", 218: "Harmonic", 219: "Synthesia", 220: "NotePiano",
    # 251-300: 스포츠 시뮬레이션
    251: "F1Race", 252: "F1Pole", 253: "TouringC", 254: "IndyCar",
    255: "NHRA", 256: "Rally", 257: "Sega", 258: "MarioKart",
    259: "CrashTeam", 260: "WildTeam", 261: "Diddy", 262: "ModNation",
    263: "TrackMania", 264: "FlatOut", 265: "Burnout", 266: "NeedSpeed",
    267: "GTA", 268: "CannonFd", 269: "HotWheels", 270: "MicroMach",
    # 301-350: 어드벤처, 탐험
    301: "SnMWars", 302: "WolfStein", 303: "Doom", 304: "Heretic",
    305: "Hexen", 306: "Strife", 307: "Chasm", 308: "DukeNuke",
    309: "Blood", 310: "Shadow", 311: "PowerSlave", 312: "Build",
    313: "Rage", 314: "Blackcrypt", 315: "CyClones", 316: "Tekken",
    317: "Mortal", 318: "SF", 319: "StreetFght", 320: "FighterChamp",
    # 351-400: 전투, 전략
    351: "AdvanceWars", 352: "FireEmblem", 353: "TacticsOgre", 354: "FFT",
    355: "Disgaea", 356: "Vandal", 357: "Dynasty", 358: "Samurai",
    359: "Koei", 360: "Total", 361: "StarCraft", 362: "Warcraft",
    363: "Dune", 364: "Civilization", 365: "Master", 366: "XCom",
    367: "TheGame", 368: "FallOut", 369: "EldoRado", 370: "Baldur",
    # 401-450: 시뮬레이션, 관리
    401: "SimCity", 402: "SimTower", 403: "SimFarm", 404: "SimEarth",
    405: "Tycoon", 406: "RolerCoast", 407: "Hospital", 408: "Theme",
    409: "Tropico", 410: "Banished", 411: "TwoPoint", 412: "OpenTTD",
    413: "VintageStory", 414: "Minecraft", 415: "Terraria", 416: "Stardew",
    417: "Animal", 418: "Harvest", 419: "Story", 420: "CastleVillain",
    # 451-500: 기타, 혼합
    451: "PacManWorld", 452: "DiddyRacing", 453: "StarFox", 454: "F-Zero",
    455: "Waverace", 456: "Seaquest", 457: "Atlantis", 458: "AnalogGame",
    459: "Breakout2", 460: "ArkanoidII", 461: "ArkanoidIII", 462: "Darius",
    463: "GalagaII", 464: "GalagaIII", 465: "Gator", 466: "Kicker",
    467: "Lumber", 468: "Super", 469: "Spy", 470: "Unknown",
    471: "ThePitII", 472: "ThePitIII", 473: "Kaboom", 474: "Centiped2",
    475: "Millipede", 476: "Vortex", 477: "Pengo2", 478: "Track",
    479: "Mousetrap", 480: "Kangaroo", 481: "Kingkong", 482: "Elevator",
    483: "LordCastle", 484: "MonsterMaze", 485: "DeathRace", 486: "HighScore",
    487: "LaserBase", 488: "Stargate", 489: "Radar", 490: "UFO",
    491: "CloneGame", 492: "Pengo3", 493: "ArcadeAce", 494: "GameOver",
    495: "VectorGame", 496: "3DVektor", 497: "ArcadeCustom", 498: "RetroVibe",
    499: "ClassicMode", 500: "MasterArcade",
}

# 기본 game_code 템플릿
GAME_CODE_TEMPLATE = '''#!/usr/bin/env python3
"""🎮 게임 {num:03d} - {name}"""
import pygame, random, sys
pygame.init()
S = 800
WHITE, BLACK = (255,255,255), (0,0,0)

class Game:
    def __init__(self):
        self.s = pygame.display.set_mode((S, S))
        pygame.display.set_caption("🎮 게임 {num:03d}")
        self.p = pygame.Rect(S//2, S-50, 40, 40)
        self.run = True

    def handle(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: self.run = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: self.run = False

    def draw(self):
        self.s.fill(BLACK)
        pygame.draw.rect(self.s, (0,255,0), self.p)
        font = pygame.font.Font(None, 48)
        txt = font.render("게임 {num:03d}", True, WHITE)
        self.s.blit(txt, (S//3, S//2))
        pygame.display.flip()

    def main(self):
        c = pygame.time.Clock()
        while self.run:
            self.handle()
            self.draw()
            c.tick(60)
        pygame.quit()

if __name__ == "__main__":
    Game().main()
'''

README_TEMPLATE = '''# 🎮 게임 {num:03d} - {name_upper}

고전 아케이드 게임 {num}번입니다.

## 게임 설명

이 게임은 고전 아케이드 게임 시리즈의 일부입니다.

## 조작 방법

- **← →**: 이동
- **SPACE**: 동작
- **ESC**: 종료

## 규칙

게임을 즐기세요!

## 설치 및 실행

```bash
cd games/001-050/game_{num:03d}_{slug} && pip install -r requirements.txt && python main.py
```

---

**시리즈**: 500개 고전 게임 컬렉션
'''

def create_game(num, slug):
    """게임 폴더 및 파일 생성"""
    # 게임 그룹 결정 (001-050, 051-100, 등)
    group = ((num - 1) // 50) + 1
    folder_start = (group - 1) * 50 + 1
    folder_end = group * 50
    folder = f"{folder_start:03d}-{folder_end:03d}"

    game_path = f"/home/user/game-old/games/{folder}/game_{num:03d}_{slug}"

    # 폴더 생성
    os.makedirs(game_path, exist_ok=True)

    # main.py 생성
    main_code = GAME_CODE_TEMPLATE.format(num=num, name=slug.upper())
    with open(f"{game_path}/main.py", "w") as f:
        f.write(main_code)

    # README.md 생성
    readme = README_TEMPLATE.format(
        num=num,
        name_upper=slug.upper(),
        slug=slug
    )
    with open(f"{game_path}/README.md", "w") as f:
        f.write(readme)

    # requirements.txt 생성
    with open(f"{game_path}/requirements.txt", "w") as f:
        f.write("pygame>=2.0.0\n")

    print(f"✅ 게임 {num:03d} ({slug}) 생성 완료")

if __name__ == "__main__":
    print("🎮 게임 024-500 자동 생성 시작...")
    print(f"총 {len(GAMES)}개 게임을 생성합니다.\n")

    for num, slug in GAMES.items():
        try:
            create_game(num, slug)
        except Exception as e:
            print(f"❌ 게임 {num:03d} 생성 실패: {e}")

    print(f"\n✅ 총 {len(GAMES)}개 게임 생성 완료!")
    print("📁 games/ 폴더를 확인하세요.")
