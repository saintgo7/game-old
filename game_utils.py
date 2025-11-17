#!/usr/bin/env python3
"""
공유 게임 유틸리티 모듈
- 점수 저장/로드
- 게임 설정
- 공통 함수들
"""
import json
import os
from pathlib import Path
from datetime import datetime

class ScoreManager:
    """하이스코어 관리"""

    def __init__(self, game_name):
        self.game_name = game_name
        self.scores_dir = Path.home() / ".arcade_games" / "scores"
        self.scores_dir.mkdir(parents=True, exist_ok=True)
        self.score_file = self.scores_dir / f"{game_name}.json"
        self.max_scores = 10
        self.scores = self.load_scores()

    def load_scores(self):
        """점수 로드"""
        if self.score_file.exists():
            try:
                with open(self.score_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def add_score(self, player_name, score):
        """점수 추가"""
        self.scores.append({
            "name": player_name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:self.max_scores]
        self.save_scores()
        return self.get_rank(score)

    def get_rank(self, score):
        """현재 점수의 순위"""
        for i, s in enumerate(self.scores):
            if s["score"] <= score:
                return i + 1
        return len(self.scores) + 1

    def is_high_score(self, score):
        """하이스코어 여부"""
        return len(self.scores) < self.max_scores or score > self.scores[-1]["score"]

    def save_scores(self):
        """점수 저장"""
        with open(self.score_file, 'w') as f:
            json.dump(self.scores, f, indent=2)

    def get_top_scores(self):
        """상위 점수 반환"""
        return self.scores[:self.max_scores]


class GameConfig:
    """게임 설정 관리"""

    def __init__(self, game_name):
        self.game_name = game_name
        self.config_dir = Path.home() / ".arcade_games" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / f"{game_name}.json"
        self.defaults = {
            "volume": 100,
            "music_volume": 80,
            "difficulty": "normal",
            "fullscreen": False,
            "player_name": "Player",
            "theme": "default"
        }
        self.config = self.load_config()

    def load_config(self):
        """설정 로드"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.defaults.copy()
        return self.defaults.copy()

    def save_config(self):
        """설정 저장"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        """설정값 가져오기"""
        return self.config.get(key, default or self.defaults.get(key))

    def set(self, key, value):
        """설정값 설정"""
        self.config[key] = value
        self.save_config()


class GameState:
    """게임 상태 관리"""

    def __init__(self):
        self.paused = False
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lives = 3

    def pause(self):
        """게임 일시정지"""
        self.paused = True

    def resume(self):
        """게임 재개"""
        self.paused = False

    def reset(self):
        """상태 초기화"""
        self.paused = False
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lives = 3


class Difficulty:
    """난이도 시스템"""

    EASY = {"speed": 0.7, "spawn_rate": 1.5, "score_mult": 0.8}
    NORMAL = {"speed": 1.0, "spawn_rate": 1.0, "score_mult": 1.0}
    HARD = {"speed": 1.3, "spawn_rate": 0.7, "score_mult": 1.5}
    EXTREME = {"speed": 1.7, "spawn_rate": 0.5, "score_mult": 2.0}

    @staticmethod
    def get_config(difficulty):
        """난이도 설정 반환"""
        configs = {
            "easy": Difficulty.EASY,
            "normal": Difficulty.NORMAL,
            "hard": Difficulty.HARD,
            "extreme": Difficulty.EXTREME
        }
        return configs.get(difficulty.lower(), Difficulty.NORMAL)


def format_score(score):
    """점수 포매팅"""
    return f"{score:,}"


def format_time(seconds):
    """시간 포매팅 (MM:SS)"""
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"


def clamp(value, min_val, max_val):
    """값 범위 제한"""
    return max(min_val, min(value, max_val))
