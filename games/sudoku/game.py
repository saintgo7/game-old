#!/usr/bin/env python3
"""
게임 메인 파일
"""
import sys
import os
import glob

# 부모 디렉토리를 Python 경로에 추가
parent_dir = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, parent_dir)

# config에서 게임 ID 읽기
config_path = os.path.join(os.path.dirname(__file__), 'config.py')
with open(config_path) as f:
    content = f.read()
    game_id_str = content.split('GAME_ID = ')[1].split('\n')[0]
    game_id = int(game_id_str)

folder_name = os.path.basename(os.path.dirname(__file__))

# 게임 파일 찾기
game_file_pattern = os.path.join(parent_dir, f"game_{game_id:03d}_{folder_name}_*.py")
game_files = glob.glob(game_file_pattern)

if game_files:
    game_file = game_files[0]  # 첫 번째 파일 사용
    
    # 게임 모듈 동적 import
    import importlib.util
    spec = importlib.util.spec_from_file_location("game_module", game_file)
    game_module = importlib.util.module_from_spec(spec)
    sys.modules["game_module"] = game_module
    spec.loader.exec_module(game_module)
    
    # 게임 클래스 찾기 및 실행
    for attr_name in dir(game_module):
        attr = getattr(game_module, attr_name)
        if isinstance(attr, type) and attr_name.endswith("Game"):
            game = attr()
            game.run()
            break
else:
    print(f"게임 파일을 찾을 수 없습니다: {game_file_pattern}")
    sys.exit(1)
