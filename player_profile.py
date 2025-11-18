#!/usr/bin/env python3
"""
플레이어 프로필 및 계정 시스템
- 플레이어 프로필 관리
- 게임 통계 추적
- 플레이어 저장/로드
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PlayerProfile:
    """플레이어 프로필"""

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.created_at = datetime.now().isoformat()
        self.last_played = datetime.now().isoformat()

        # 통계
        self.stats = {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "total_score": 0,
            "best_score": 0,
            "total_playtime": 0,  # 초 단위
            "games_played": {}  # 게임별 통계
        }

        # 성과/뱃지
        self.achievements = []
        self.unlocked_badges = []

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "player_id": self.player_id,
            "name": self.name,
            "created_at": self.created_at,
            "last_played": self.last_played,
            "stats": self.stats,
            "achievements": self.achievements,
            "unlocked_badges": self.unlocked_badges
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리에서 로드"""
        profile = PlayerProfile(data["player_id"], data["name"])
        profile.created_at = data.get("created_at", profile.created_at)
        profile.last_played = data.get("last_played", profile.last_played)
        profile.stats = data.get("stats", profile.stats)
        profile.achievements = data.get("achievements", [])
        profile.unlocked_badges = data.get("unlocked_badges", [])
        return profile

    def update_last_played(self):
        """마지막 플레이 시간 업데이트"""
        self.last_played = datetime.now().isoformat()

    def record_game(self, game_name, score, won, playtime):
        """게임 결과 기록"""
        self.stats["total_games"] += 1
        self.stats["total_score"] += score
        self.stats["total_playtime"] += playtime

        if score > self.stats["best_score"]:
            self.stats["best_score"] = score

        if won:
            self.stats["wins"] += 1
        else:
            self.stats["losses"] += 1

        # 게임별 통계
        if game_name not in self.stats["games_played"]:
            self.stats["games_played"][game_name] = {
                "plays": 0,
                "wins": 0,
                "best_score": 0
            }

        game_stats = self.stats["games_played"][game_name]
        game_stats["plays"] += 1
        if won:
            game_stats["wins"] += 1
        if score > game_stats["best_score"]:
            game_stats["best_score"] = score

        self.update_last_played()

    def add_achievement(self, achievement):
        """성과 추가"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def unlock_badge(self, badge):
        """뱃지 해제"""
        if badge not in self.unlocked_badges:
            self.unlocked_badges.append(badge)

    def get_win_rate(self):
        """승률 계산"""
        total = self.stats["total_games"]
        if total == 0:
            return 0.0
        return (self.stats["wins"] / total) * 100

    def get_average_score(self):
        """평균 점수 계산"""
        total = self.stats["total_games"]
        if total == 0:
            return 0
        return self.stats["total_score"] // total

    def get_total_playtime_hours(self):
        """총 플레이 시간 (시간)"""
        return self.stats["total_playtime"] / 3600


class PlayerProfileManager:
    """플레이어 프로필 관리자"""

    def __init__(self, save_dir="profiles"):
        self.save_dir = save_dir
        self.profiles: Dict[str, PlayerProfile] = {}
        self.current_player: Optional[PlayerProfile] = None

        # 저장 디렉토리 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 기존 프로필 로드
        self.load_all_profiles()

    def _get_profile_path(self, player_id):
        """프로필 파일 경로"""
        return os.path.join(self.save_dir, f"{player_id}.json")

    def create_profile(self, player_id, name):
        """새 프로필 생성"""
        if player_id in self.profiles:
            return self.profiles[player_id]

        profile = PlayerProfile(player_id, name)
        self.profiles[player_id] = profile
        self.save_profile(player_id)
        return profile

    def get_profile(self, player_id):
        """프로필 가져오기"""
        return self.profiles.get(player_id)

    def load_all_profiles(self):
        """모든 프로필 로드"""
        if not os.path.exists(self.save_dir):
            return

        for filename in os.listdir(self.save_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.save_dir, filename), 'r') as f:
                        data = json.load(f)
                        profile = PlayerProfile.from_dict(data)
                        self.profiles[profile.player_id] = profile
                except Exception as e:
                    print(f"프로필 로드 실패: {filename} - {e}")

    def save_profile(self, player_id):
        """프로필 저장"""
        if player_id not in self.profiles:
            return False

        try:
            profile = self.profiles[player_id]
            path = self._get_profile_path(player_id)
            with open(path, 'w') as f:
                json.dump(profile.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"프로필 저장 실패: {player_id} - {e}")
            return False

    def save_all_profiles(self):
        """모든 프로필 저장"""
        for player_id in self.profiles:
            self.save_profile(player_id)

    def login(self, player_id):
        """플레이어 로그인"""
        if player_id in self.profiles:
            self.current_player = self.profiles[player_id]
            self.current_player.update_last_played()
            return self.current_player
        return None

    def logout(self):
        """플레이어 로그아웃"""
        if self.current_player:
            self.save_profile(self.current_player.player_id)
        self.current_player = None

    def get_current_player(self):
        """현재 플레이어 반환"""
        return self.current_player

    def delete_profile(self, player_id):
        """프로필 삭제"""
        if player_id in self.profiles:
            path = self._get_profile_path(player_id)
            if os.path.exists(path):
                os.remove(path)
            del self.profiles[player_id]
            return True
        return False

    def get_all_profiles(self):
        """모든 프로필 반환"""
        return list(self.profiles.values())

    def get_leaderboard(self, metric="best_score", limit=10):
        """리더보드 생성"""
        profiles = list(self.profiles.values())

        if metric == "best_score":
            sorted_profiles = sorted(profiles,
                                    key=lambda p: p.stats["best_score"],
                                    reverse=True)
        elif metric == "wins":
            sorted_profiles = sorted(profiles,
                                    key=lambda p: p.stats["wins"],
                                    reverse=True)
        elif metric == "win_rate":
            sorted_profiles = sorted(profiles,
                                    key=lambda p: p.get_win_rate(),
                                    reverse=True)
        else:
            sorted_profiles = profiles

        return [(p.name, getattr(p.stats, metric, 0)) for p in sorted_profiles[:limit]]

    def get_game_leaderboard(self, game_name, limit=10):
        """게임별 리더보드"""
        profiles = []
        for profile in self.profiles.values():
            if game_name in profile.stats["games_played"]:
                best_score = profile.stats["games_played"][game_name]["best_score"]
                profiles.append((profile.name, best_score))

        profiles.sort(key=lambda x: x[1], reverse=True)
        return profiles[:limit]

    def get_top_players(self, limit=10):
        """상위 플레이어"""
        return self.get_leaderboard("best_score", limit)

    def get_statistics_summary(self):
        """통계 요약"""
        total_players = len(self.profiles)
        total_games = sum(p.stats["total_games"] for p in self.profiles.values())
        avg_best_score = sum(p.stats["best_score"] for p in self.profiles.values()) / max(1, total_players)

        return {
            "total_players": total_players,
            "total_games": total_games,
            "average_best_score": int(avg_best_score)
        }


# 글로벌 플레이어 관리자
_global_profile_manager = None


def get_profile_manager():
    """글로벌 플레이어 관리자 반환"""
    global _global_profile_manager
    if _global_profile_manager is None:
        _global_profile_manager = PlayerProfileManager()
    return _global_profile_manager
