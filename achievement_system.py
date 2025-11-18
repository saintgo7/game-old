#!/usr/bin/env python3
"""
성과 및 뱃지 시스템
- 게임별 성과 정의
- 플레이어 뱃지 추적
- 성과 달성 조건
"""
from enum import Enum
from typing import Dict, List
from datetime import datetime


class BadgeType(Enum):
    """뱃지 타입"""
    # 진행도
    FIRST_GAME = "첫 게임"
    LEVEL_5 = "5레벨 달성"
    LEVEL_10 = "10레벨 달성"

    # 점수
    SCORE_100 = "100점 달성"
    SCORE_1000 = "1,000점 달성"
    SCORE_10000 = "10,000점 달성"

    # 게임별
    SHOOTER_MASTER = "발사 게임 마스터"
    RACER_MASTER = "레이싱 게임 마스터"
    PUZZLE_MASTER = "퍼즐 게임 마스터"
    RPG_MASTER = "RPG 마스터"
    FIGHTER_MASTER = "격투 게임 마스터"
    BOARD_MASTER = "보드 게임 마스터"

    # 특별
    SPEEDRUN = "빠른 클리어"
    PERFECT_GAME = "완벽한 게임"
    COMEBACK = "역전 승리"
    UNBEATABLE = "무적"


class Badge:
    """뱃지"""

    def __init__(self, badge_type: BadgeType, description: str = "", icon: str = "🏆"):
        self.type = badge_type
        self.name = badge_type.value
        self.description = description
        self.icon = icon
        self.unlocked_at = None

    def unlock(self):
        """뱃지 해제"""
        if not self.unlocked_at:
            self.unlocked_at = datetime.now().isoformat()
            return True
        return False

    def is_unlocked(self):
        """해제 여부"""
        return self.unlocked_at is not None

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "type": self.type.name,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "unlocked_at": self.unlocked_at
        }


class Achievement:
    """성과"""

    def __init__(self, name: str, description: str, badge_type: BadgeType,
                 condition_func=None):
        self.name = name
        self.description = description
        self.badge_type = badge_type
        self.condition_func = condition_func  # 달성 조건을 확인하는 함수
        self.progress = 0
        self.max_progress = 100
        self.completed = False
        self.completed_at = None

    def check_completion(self, **kwargs):
        """완료 조건 확인"""
        if self.completed:
            return False

        if self.condition_func and self.condition_func(**kwargs):
            self.completed = True
            self.completed_at = datetime.now().isoformat()
            self.progress = self.max_progress
            return True

        return False

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "name": self.name,
            "description": self.description,
            "badge_type": self.badge_type.name,
            "progress": self.progress,
            "max_progress": self.max_progress,
            "completed": self.completed,
            "completed_at": self.completed_at
        }


class AchievementManager:
    """성과 관리"""

    def __init__(self):
        self.badges: Dict[str, Badge] = {}
        self.achievements: Dict[str, Achievement] = {}
        self._initialize_badges()
        self._initialize_achievements()

    def _initialize_badges(self):
        """뱃지 초기화"""
        badge_definitions = [
            (BadgeType.FIRST_GAME, "처음으로 게임을 시작했다", "🎮"),
            (BadgeType.LEVEL_5, "레벨 5에 도달했다", "⭐"),
            (BadgeType.LEVEL_10, "레벨 10에 도달했다", "⭐⭐"),
            (BadgeType.SCORE_100, "100점을 얻었다", "💯"),
            (BadgeType.SCORE_1000, "1,000점을 얻었다", "🔥"),
            (BadgeType.SCORE_10000, "10,000점을 얻었다", "💎"),
            (BadgeType.SHOOTER_MASTER, "발사 게임에 능숙해졌다", "🔫"),
            (BadgeType.RACER_MASTER, "레이싱 게임을 마스터했다", "🏎️"),
            (BadgeType.PUZZLE_MASTER, "퍼즐 게임을 마스터했다", "🧩"),
            (BadgeType.RPG_MASTER, "RPG 게임을 마스터했다", "🏰"),
            (BadgeType.FIGHTER_MASTER, "격투 게임을 마스터했다", "🥊"),
            (BadgeType.BOARD_MASTER, "보드 게임을 마스터했다", "♟️"),
            (BadgeType.SPEEDRUN, "빠르게 게임을 클리어했다", "⚡"),
            (BadgeType.PERFECT_GAME, "완벽한 게임을 했다", "✨"),
            (BadgeType.COMEBACK, "역전 승리를 거두었다", "🎯"),
            (BadgeType.UNBEATABLE, "무적의 상태가 되었다", "👑"),
        ]

        for badge_type, description, icon in badge_definitions:
            self.badges[badge_type.name] = Badge(badge_type, description, icon)

    def _initialize_achievements(self):
        """성과 초기화"""
        achievements = [
            Achievement("첫 시작", "처음 게임을 시작하기",
                       BadgeType.FIRST_GAME,
                       lambda games_played=0, **kwargs: games_played > 0),

            Achievement("레벨 5", "레벨 5에 도달하기",
                       BadgeType.LEVEL_5,
                       lambda level=0, **kwargs: level >= 5),

            Achievement("레벨 10", "레벨 10에 도달하기",
                       BadgeType.LEVEL_10,
                       lambda level=0, **kwargs: level >= 10),

            Achievement("백점", "한 게임에서 100점 이상 얻기",
                       BadgeType.SCORE_100,
                       lambda score=0, **kwargs: score >= 100),

            Achievement("천점", "한 게임에서 1,000점 이상 얻기",
                       BadgeType.SCORE_1000,
                       lambda score=0, **kwargs: score >= 1000),

            Achievement("만점", "한 게임에서 10,000점 이상 얻기",
                       BadgeType.SCORE_10000,
                       lambda score=0, **kwargs: score >= 10000),

            Achievement("발사 마스터", "발사 게임 5개 클리어",
                       BadgeType.SHOOTER_MASTER,
                       lambda shooting_wins=0, **kwargs: shooting_wins >= 5),

            Achievement("레이싱 마스터", "레이싱 게임 5개 클리어",
                       BadgeType.RACER_MASTER,
                       lambda racing_wins=0, **kwargs: racing_wins >= 5),

            Achievement("퍼즐 마스터", "퍼즐 게임 5개 클리어",
                       BadgeType.PUZZLE_MASTER,
                       lambda puzzle_wins=0, **kwargs: puzzle_wins >= 5),

            Achievement("RPG 마스터", "RPG 게임 5개 클리어",
                       BadgeType.RPG_MASTER,
                       lambda rpg_wins=0, **kwargs: rpg_wins >= 5),

            Achievement("격투 마스터", "격투 게임 5개 클리어",
                       BadgeType.FIGHTER_MASTER,
                       lambda fighter_wins=0, **kwargs: fighter_wins >= 5),

            Achievement("보드 마스터", "보드 게임 5개 클리어",
                       BadgeType.BOARD_MASTER,
                       lambda board_wins=0, **kwargs: board_wins >= 5),
        ]

        for i, achievement in enumerate(achievements):
            self.achievements[f"achievement_{i}"] = achievement

    def unlock_badge(self, badge_type: BadgeType):
        """뱃지 해제"""
        if badge_type.name in self.badges:
            return self.badges[badge_type.name].unlock()
        return False

    def check_achievements(self, **kwargs):
        """성과 달성 확인"""
        unlocked = []
        for key, achievement in self.achievements.items():
            if achievement.check_completion(**kwargs):
                self.unlock_badge(achievement.badge_type)
                unlocked.append(achievement)

        return unlocked

    def get_unlocked_badges(self):
        """해제된 뱃지"""
        return [badge for badge in self.badges.values() if badge.is_unlocked()]

    def get_badge_count(self):
        """뱃지 개수"""
        return len(self.get_unlocked_badges())

    def get_total_badge_count(self):
        """전체 뱃지 개수"""
        return len(self.badges)

    def get_progress(self):
        """진행률 (%)"""
        total = self.get_total_badge_count()
        if total == 0:
            return 0
        return (self.get_badge_count() / total) * 100

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "badges": {k: v.to_dict() for k, v in self.badges.items()},
            "achievements": {k: v.to_dict() for k, v in self.achievements.items()}
        }

    def get_summary(self):
        """요약 정보"""
        return {
            "unlocked_badges": self.get_badge_count(),
            "total_badges": self.get_total_badge_count(),
            "progress_percent": self.get_progress(),
            "badges": [b.name for b in self.get_unlocked_badges()]
        }


# 글로벌 성과 관리자
_global_achievement_manager = None


def get_achievement_manager():
    """글로벌 성과 관리자 반환"""
    global _global_achievement_manager
    if _global_achievement_manager is None:
        _global_achievement_manager = AchievementManager()
    return _global_achievement_manager
