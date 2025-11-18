#!/usr/bin/env python3
"""
통계 관리 시스템
- 게임별 통계 추적
- 플레이어 리더보드
- 시즌 기록
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


class GameStatistics:
    """게임별 통계"""

    def __init__(self, game_name: str):
        self.game_name = game_name
        self.plays = 0
        self.wins = 0
        self.losses = 0
        self.total_score = 0
        self.best_score = 0
        self.total_time = 0  # 초
        self.first_played = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()

    def record_game(self, score: int, won: bool, playtime: int):
        """게임 기록"""
        self.plays += 1
        self.total_score += score
        self.total_time += playtime
        self.last_played = datetime.now().isoformat()

        if won:
            self.wins += 1
        else:
            self.losses += 1

        if score > self.best_score:
            self.best_score = score

    def get_win_rate(self):
        """승률"""
        if self.plays == 0:
            return 0.0
        return (self.wins / self.plays) * 100

    def get_average_score(self):
        """평균 점수"""
        if self.plays == 0:
            return 0
        return self.total_score // self.plays

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "game_name": self.game_name,
            "plays": self.plays,
            "wins": self.wins,
            "losses": self.losses,
            "total_score": self.total_score,
            "best_score": self.best_score,
            "total_time": self.total_time,
            "first_played": self.first_played,
            "last_played": self.last_played,
            "win_rate": self.get_win_rate(),
            "average_score": self.get_average_score()
        }


class StatisticsManager:
    """통계 관리자"""

    def __init__(self, save_dir="statistics"):
        self.save_dir = save_dir
        self.game_stats: Dict[str, GameStatistics] = {}
        self.global_stats = {
            "total_games": 0,
            "total_wins": 0,
            "total_losses": 0,
            "total_score": 0,
            "total_playtime": 0
        }

        # 저장 디렉토리 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        self.load_statistics()

    def record_game(self, game_name: str, score: int, won: bool, playtime: int):
        """게임 기록"""
        # 게임별 통계 업데이트
        if game_name not in self.game_stats:
            self.game_stats[game_name] = GameStatistics(game_name)

        self.game_stats[game_name].record_game(score, won, playtime)

        # 전역 통계 업데이트
        self.global_stats["total_games"] += 1
        self.global_stats["total_score"] += score
        self.global_stats["total_playtime"] += playtime

        if won:
            self.global_stats["total_wins"] += 1
        else:
            self.global_stats["total_losses"] += 1

        self.save_statistics()

    def get_game_statistics(self, game_name: str):
        """게임 통계"""
        return self.game_stats.get(game_name)

    def get_all_game_statistics(self):
        """모든 게임 통계"""
        return list(self.game_stats.values())

    def get_leaderboard(self, metric: str = "best_score", limit: int = 10):
        """리더보드"""
        games = list(self.game_stats.values())

        if metric == "best_score":
            games.sort(key=lambda g: g.best_score, reverse=True)
        elif metric == "plays":
            games.sort(key=lambda g: g.plays, reverse=True)
        elif metric == "wins":
            games.sort(key=lambda g: g.wins, reverse=True)
        elif metric == "win_rate":
            games.sort(key=lambda g: g.get_win_rate(), reverse=True)
        else:
            games.sort(key=lambda g: g.best_score, reverse=True)

        result = []
        for i, game in enumerate(games[:limit], 1):
            if metric == "best_score":
                value = game.best_score
            elif metric == "plays":
                value = game.plays
            elif metric == "wins":
                value = game.wins
            elif metric == "win_rate":
                value = f"{game.get_win_rate():.1f}%"
            else:
                value = game.best_score

            result.append((i, game.game_name, value))

        return result

    def get_top_games(self, limit: int = 5):
        """상위 게임"""
        return self.get_leaderboard("best_score", limit)

    def get_most_played_games(self, limit: int = 5):
        """가장 많이 플레이된 게임"""
        return self.get_leaderboard("plays", limit)

    def get_global_statistics(self):
        """전역 통계"""
        total_games = self.global_stats["total_games"]
        total_wins = self.global_stats["total_wins"]
        total_score = self.global_stats["total_score"]
        total_playtime = self.global_stats["total_playtime"]

        win_rate = (total_wins / total_games * 100) if total_games > 0 else 0
        avg_score = (total_score // total_games) if total_games > 0 else 0
        avg_playtime = (total_playtime // total_games) if total_games > 0 else 0

        return {
            "total_games": total_games,
            "total_wins": total_wins,
            "total_losses": total_games - total_wins,
            "win_rate": win_rate,
            "total_score": total_score,
            "average_score": avg_score,
            "total_playtime": total_playtime,
            "average_playtime": avg_playtime,
            "total_hours": total_playtime / 3600
        }

    def save_statistics(self):
        """통계 저장"""
        try:
            data = {
                "global": self.global_stats,
                "games": {name: stats.to_dict() for name, stats in self.game_stats.items()}
            }

            filepath = os.path.join(self.save_dir, "statistics.json")
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"통계 저장 실패: {e}")
            return False

    def load_statistics(self):
        """통계 로드"""
        try:
            filepath = os.path.join(self.save_dir, "statistics.json")
            if not os.path.exists(filepath):
                return

            with open(filepath, 'r') as f:
                data = json.load(f)

            # 전역 통계
            self.global_stats = data.get("global", self.global_stats)

            # 게임 통계
            for game_name, stats_data in data.get("games", {}).items():
                stats = GameStatistics(game_name)
                stats.plays = stats_data.get("plays", 0)
                stats.wins = stats_data.get("wins", 0)
                stats.losses = stats_data.get("losses", 0)
                stats.total_score = stats_data.get("total_score", 0)
                stats.best_score = stats_data.get("best_score", 0)
                stats.total_time = stats_data.get("total_time", 0)
                stats.first_played = stats_data.get("first_played", "")
                stats.last_played = stats_data.get("last_played", "")
                self.game_stats[game_name] = stats

            return True
        except Exception as e:
            print(f"통계 로드 실패: {e}")
            return False

    def reset_statistics(self):
        """통계 초기화"""
        self.game_stats = {}
        self.global_stats = {
            "total_games": 0,
            "total_wins": 0,
            "total_losses": 0,
            "total_score": 0,
            "total_playtime": 0
        }
        self.save_statistics()

    def export_statistics(self, filename: str = "statistics_export.json"):
        """통계 내보내기"""
        try:
            data = {
                "exported_at": datetime.now().isoformat(),
                "global": self.get_global_statistics(),
                "games": [stats.to_dict() for stats in self.get_all_game_statistics()]
            }

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"통계 내보내기 실패: {e}")
            return False


# 글로벌 통계 관리자
_global_statistics_manager = None


def get_statistics_manager():
    """글로벌 통계 관리자 반환"""
    global _global_statistics_manager
    if _global_statistics_manager is None:
        _global_statistics_manager = StatisticsManager()
    return _global_statistics_manager
