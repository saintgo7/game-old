#!/usr/bin/env python3
"""
멀티플레이 시스템 (로컬 및 네트워크, 향상된 버전)
- 로컬 멀티플레이 (splitscreen)
- 네트워크 멀티플레이
- 게임 상태 동기화
- 매치메이킹
"""
import socket
import json
from enum import Enum
from datetime import datetime
import pygame


class GameMode(Enum):
    """게임 모드"""
    SINGLE_PLAYER = 1
    LOCAL_MULTIPLAYER = 2
    NETWORK_MULTIPLAYER = 3


class Player:
    """플레이어 정보"""

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.score = 0
        self.lives = 3
        self.ready = False
        self.connected = True

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "player_id": self.player_id,
            "name": self.name,
            "score": self.score,
            "lives": self.lives,
            "ready": self.ready,
            "connected": self.connected
        }

    def from_dict(self, data):
        """딕셔너리에서 로드"""
        self.score = data.get("score", 0)
        self.lives = data.get("lives", 3)
        self.ready = data.get("ready", False)
        self.connected = data.get("connected", True)


class LocalMultiplayer:
    """로컬 멀티플레이 (같은 컴퓨터)"""

    def __init__(self, num_players=2):
        self.num_players = num_players
        self.players = []
        self.current_player = 0
        self.mode = GameMode.LOCAL_MULTIPLAYER

        for i in range(num_players):
            player = Player(i, f"Player {i + 1}")
            self.players.append(player)

    def next_player(self):
        """다음 플레이어로 전환"""
        self.current_player = (self.current_player + 1) % self.num_players

    def get_current_player(self):
        """현재 플레이어 반환"""
        return self.players[self.current_player]

    def get_scores(self):
        """모든 플레이어의 점수"""
        return [(p.name, p.score) for p in self.players]

    def get_winner(self):
        """우승자 반환"""
        return max(self.players, key=lambda p: p.score)

    def update_score(self, points):
        """점수 업데이트"""
        self.players[self.current_player].score += points

    def get_leaderboard(self):
        """순위표"""
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        return [(p.name, p.score) for p in sorted_players]


class NetworkMultiplayer:
    """네트워크 멀티플레이"""

    def __init__(self, is_server=False, host="localhost", port=5000):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.socket = None
        self.connected_clients = []
        self.players = {}
        self.mode = GameMode.NETWORK_MULTIPLAYER

    def start_server(self):
        """서버 시작"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"서버 시작: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"서버 시작 실패: {e}")
            return False

    def connect_to_server(self):
        """서버에 연결"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"서버 연결: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"서버 연결 실패: {e}")
            return False

    def send_data(self, data):
        """데이터 전송"""
        try:
            message = json.dumps(data)
            self.socket.send(message.encode())
            return True
        except Exception as e:
            print(f"데이터 전송 실패: {e}")
            return False

    def receive_data(self):
        """데이터 수신"""
        try:
            data = self.socket.recv(1024).decode()
            return json.loads(data)
        except Exception as e:
            print(f"데이터 수신 실패: {e}")
            return None

    def broadcast(self, data):
        """모든 클라이언트에게 브로드캐스트"""
        message = json.dumps(data)
        for client in self.connected_clients:
            try:
                client.send(message.encode())
            except:
                self.connected_clients.remove(client)

    def close(self):
        """연결 종료"""
        if self.socket:
            self.socket.close()


class GameSync:
    """게임 상태 동기화 (향상된 버전)"""

    def __init__(self):
        self.state = {
            "game_over": False,
            "scores": {},
            "timestamp": None,
            "round": 1,
            "game_time": 0,
            "paused": False
        }
        self.sync_interval = 50  # 50ms마다 동기화
        self.last_sync = datetime.now()

    def update_state(self, data):
        """상태 업데이트"""
        self.state.update(data)
        self.state["timestamp"] = datetime.now().isoformat()

    def should_sync(self):
        """동기화해야 하는지 확인"""
        elapsed = (datetime.now() - self.last_sync).total_seconds() * 1000
        return elapsed >= self.sync_interval

    def mark_synced(self):
        """동기화 완료 표시"""
        self.last_sync = datetime.now()

    def get_state(self):
        """상태 반환"""
        return self.state.copy()

    def reset_state(self):
        """상태 초기화"""
        self.state = {
            "game_over": False,
            "scores": {},
            "timestamp": None,
            "round": 1,
            "game_time": 0,
            "paused": False
        }
        self.last_sync = datetime.now()

    def add_score(self, player_id, points):
        """플레이어 점수 추가"""
        if player_id not in self.state["scores"]:
            self.state["scores"][player_id] = 0
        self.state["scores"][player_id] += points

    def get_leaderboard(self):
        """순위표 반환"""
        scores = self.state["scores"]
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


class Matchmaking:
    """매치메이킹 시스템"""

    def __init__(self, min_players=2, max_players=4):
        self.min_players = min_players
        self.max_players = max_players
        self.waiting_players = []
        self.active_matches = []

    def add_player(self, player):
        """플레이어 추가"""
        self.waiting_players.append(player)
        if len(self.waiting_players) >= self.min_players:
            return self.create_match()
        return None

    def create_match(self):
        """매치 생성"""
        if len(self.waiting_players) < self.min_players:
            return None

        match_players = self.waiting_players[:self.max_players]
        self.waiting_players = self.waiting_players[self.max_players:]

        match = {
            "id": len(self.active_matches),
            "players": match_players,
            "created_at": datetime.now().isoformat(),
            "status": "in_progress"
        }

        self.active_matches.append(match)
        return match

    def end_match(self, match_id):
        """매치 종료"""
        for match in self.active_matches:
            if match["id"] == match_id:
                match["status"] = "completed"
                return True
        return False

    def get_match(self, match_id):
        """매치 정보"""
        for match in self.active_matches:
            if match["id"] == match_id:
                return match
        return None


class SplitScreenManager:
    """로컬 멀티플레이 splitscreen 관리"""

    def __init__(self, num_players=2, screen_width=800, screen_height=600):
        self.num_players = num_players
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surfaces = []
        self.player_rects = []
        self.setup_splitscreen()

    def setup_splitscreen(self):
        """Splitscreen 설정"""
        if self.num_players == 2:
            # 좌우 분할
            half_width = self.screen_width // 2
            self.player_rects = [
                pygame.Rect(0, 0, half_width, self.screen_height),  # Player 1 (left)
                pygame.Rect(half_width, 0, half_width, self.screen_height)  # Player 2 (right)
            ]
        elif self.num_players == 4:
            # 4분할
            half_width = self.screen_width // 2
            half_height = self.screen_height // 2
            self.player_rects = [
                pygame.Rect(0, 0, half_width, half_height),  # Top-left
                pygame.Rect(half_width, 0, half_width, half_height),  # Top-right
                pygame.Rect(0, half_height, half_width, half_height),  # Bottom-left
                pygame.Rect(half_width, half_height, half_width, half_height)  # Bottom-right
            ]
        else:
            # 기본값: 2분할
            self.player_rects = [
                pygame.Rect(0, 0, self.screen_width, self.screen_height)
            ]

    def get_player_surface(self, player_id):
        """플레이어별 서브서피스 반환"""
        if 0 <= player_id < len(self.player_rects):
            return self.player_rects[player_id]
        return None

    def draw_borders(self, surface):
        """분할 경계선 그리기"""
        if self.num_players == 2:
            # 수직선
            pygame.draw.line(surface, (128, 128, 128),
                           (self.screen_width // 2, 0),
                           (self.screen_width // 2, self.screen_height), 2)
        elif self.num_players == 4:
            # 수직선
            pygame.draw.line(surface, (128, 128, 128),
                           (self.screen_width // 2, 0),
                           (self.screen_width // 2, self.screen_height), 2)
            # 수평선
            pygame.draw.line(surface, (128, 128, 128),
                           (0, self.screen_height // 2),
                           (self.screen_width, self.screen_height // 2), 2)

    def blit_player_view(self, main_surface, player_id, player_surface):
        """플레이어 뷰를 메인 서피스에 그리기"""
        if 0 <= player_id < len(self.player_rects):
            rect = self.player_rects[player_id]
            # 플레이어 서피스를 해당 영역에 복사
            if player_surface:
                scaled = pygame.transform.scale(player_surface,
                                              (rect.width, rect.height))
                main_surface.blit(scaled, rect)


class InputHandler:
    """멀티플레이 입력 처리"""

    # 플레이어 1 키 바인딩 (WASD)
    PLAYER1_KEYS = {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "action": pygame.K_SPACE
    }

    # 플레이어 2 키 바인딩 (화살표)
    PLAYER2_KEYS = {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "action": pygame.K_RETURN
    }

    @staticmethod
    def get_player_input(player_id, keys_pressed):
        """플레이어 입력 가져오기"""
        if player_id == 0:
            key_map = InputHandler.PLAYER1_KEYS
        elif player_id == 1:
            key_map = InputHandler.PLAYER2_KEYS
        else:
            return {}

        return {
            "up": keys_pressed[key_map["up"]],
            "down": keys_pressed[key_map["down"]],
            "left": keys_pressed[key_map["left"]],
            "right": keys_pressed[key_map["right"]],
            "action": keys_pressed[key_map["action"]]
        }

    @staticmethod
    def get_all_players_input(num_players, keys_pressed):
        """모든 플레이어 입력 가져오기"""
        inputs = {}
        for player_id in range(num_players):
            inputs[player_id] = InputHandler.get_player_input(player_id, keys_pressed)
        return inputs
