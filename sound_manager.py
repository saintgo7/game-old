#!/usr/bin/env python3
"""
사운드 및 음악 관리 시스템 (향상된 버전)
- 채널 관리
- 사운드 믹싱
- 페이드 효과
- 음향 이펙트 라이브러리
"""
import pygame
from pathlib import Path
import os
from enum import Enum
from typing import Dict, Optional

class SoundPriority(Enum):
    """사운드 우선순위"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class SoundManager:
    """향상된 사운드 및 음악 관리"""

    def __init__(self, volume=100, music_volume=80, num_channels=16):
        self.volume = volume
        self.music_volume = music_volume
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_music = None
        self.music_playing = False
        self.fade_duration = 0  # 음악 페이드 지속 시간

        # 채널 관리
        self.num_channels = num_channels
        self.active_channels: Dict[int, str] = {}  # 채널 ID -> 사운드 이름

        # Pygame mixer 초기화
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(num_channels)
        except:
            self.enabled = False
            return

        self.enabled = True
        self._setup_channels()

    def _setup_channels(self):
        """채널 설정"""
        if not self.enabled:
            return
        try:
            for i in range(self.num_channels):
                pygame.mixer.Channel(i).set_volume(self.volume / 100.0)
        except:
            pass

    def _get_available_channel(self, priority=SoundPriority.NORMAL):
        """사용 가능한 채널 얻기"""
        try:
            # 우선순위에 따라 채널 할당
            for i in range(self.num_channels):
                if not pygame.mixer.Channel(i).get_busy():
                    return i

            # 낮은 우선순위의 채널을 중단하고 사용
            if priority.value >= SoundPriority.HIGH.value:
                # HIGH 이상이면 LOW 채널 중단
                for i in range(self.num_channels):
                    channel = pygame.mixer.Channel(i)
                    if channel.get_busy():
                        channel.stop()
                        return i
            return 0  # 기본 채널
        except:
            return 0

    def load_sound(self, name, filepath):
        """사운드 파일 로드"""
        if not self.enabled:
            return

        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(self.volume / 100.0)
                self.sounds[name] = sound
        except Exception as e:
            print(f"사운드 로드 실패: {name} - {e}")

    def play_sound(self, name, loops=0, priority=SoundPriority.NORMAL):
        """사운드 재생 (우선순위 기반 채널 할당)"""
        if not self.enabled or name not in self.sounds:
            return

        try:
            sound = self.sounds[name]
            channel_id = self._get_available_channel(priority)
            channel = pygame.mixer.Channel(channel_id)
            channel.play(sound, loops)
            self.active_channels[channel_id] = name
        except:
            pass

    def stop_sound(self, name):
        """특정 사운드 중지"""
        if not self.enabled:
            return
        try:
            for channel_id, sound_name in self.active_channels.items():
                if sound_name == name:
                    pygame.mixer.Channel(channel_id).stop()
                    del self.active_channels[channel_id]
                    break
        except:
            pass

    def load_music(self, filepath):
        """음악 파일 로드"""
        if not self.enabled:
            return

        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume / 100.0)
                self.current_music = filepath
        except Exception as e:
            print(f"음악 로드 실패: {e}")

    def play_music(self, loops=-1, fade_ms=0):
        """음악 재생 (페이드 효과 옵션)"""
        if not self.enabled or not self.current_music:
            return

        try:
            if fade_ms > 0:
                pygame.mixer.music.play(loops, fade_ms=fade_ms)
            else:
                pygame.mixer.music.play(loops)
            self.music_playing = True
            self.fade_duration = fade_ms
        except:
            pass

    def stop_music(self, fade_ms=0):
        """음악 중지 (페이드 아웃 옵션)"""
        if not self.enabled:
            return

        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
            self.music_playing = False
        except:
            pass

    def fade_in_music(self, fade_ms=2000, loops=-1):
        """음악 페이드인 재생"""
        if not self.enabled or not self.current_music:
            return

        try:
            pygame.mixer.music.play(loops, fade_ms=fade_ms)
            self.music_playing = True
        except:
            pass

    def fade_out_music(self, fade_ms=2000):
        """음악 페이드아웃"""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.fadeout(fade_ms)
            self.music_playing = False
        except:
            pass

    def pause_music(self):
        """음악 일시정지"""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.pause()
        except:
            pass

    def resume_music(self):
        """음악 재개"""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.unpause()
        except:
            pass

    def set_volume(self, volume):
        """볼륨 설정"""
        if not self.enabled:
            return

        self.volume = max(0, min(100, volume))
        try:
            for sound in self.sounds.values():
                sound.set_volume(self.volume / 100.0)
        except:
            pass

    def set_music_volume(self, volume):
        """음악 볼륨 설정"""
        if not self.enabled:
            return

        self.music_volume = max(0, min(100, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume / 100.0)
        except:
            pass

    def is_music_playing(self):
        """음악 재생 중인지 확인"""
        if not self.enabled:
            return False

        try:
            return pygame.mixer.music.get_busy()
        except:
            return False


# 사운드 효과 라이브러리
class SoundEffects:
    """게임 사운드 효과 라이브러리"""

    # 주파수 정의 (음악 음)
    FREQUENCIES = {
        'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
        'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    }

    @staticmethod
    def create_tone(frequency, duration=100):
        """음정 생성"""
        if not pygame.mixer.get_init():
            return None

        sample_rate = 22050
        frames = int(duration * sample_rate / 1000)

        import math
        arr = []
        for i in range(frames):
            val = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            arr.append(val)

        try:
            sound = pygame.mixer.Sound(buffer=bytes(arr))
            return sound
        except:
            return None

    @staticmethod
    def create_success_sound():
        """성공 음향 (상승음)"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(523, 100)  # C5
        except:
            return None

    @staticmethod
    def create_error_sound():
        """에러 음향 (하강음)"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(220, 200)  # A3
        except:
            return None

    @staticmethod
    def create_coin_sound():
        """코인 음향"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(784, 80)  # G5
        except:
            return None

    @staticmethod
    def create_jump_sound():
        """점프 음향 (상승 후 하강)"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(587, 150)  # D5
        except:
            return None

    @staticmethod
    def create_explosion_sound():
        """폭발 음향 (저주파)"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(80, 200)  # Deep
        except:
            return None

    @staticmethod
    def create_powerup_sound():
        """파워업 음향 (상승음)"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(880, 100)  # A5
        except:
            return None

    @staticmethod
    def create_pickup_sound():
        """획득 음향"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(659, 80)  # E5
        except:
            return None

    @staticmethod
    def create_shoot_sound():
        """발사 음향"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(440, 50)  # A4 - 짧고 날카로운 음
        except:
            return None

    @staticmethod
    def create_hit_sound():
        """히트 음향"""
        if not pygame.mixer.get_init():
            return None
        try:
            return SoundEffects.create_tone(330, 100)  # E4
        except:
            return None

# 기본 사운드 효과 (하위 호환성)
class DefaultSounds:
    """기본 사운드 이펙트 생성 (레거시)"""

    @staticmethod
    def create_beep(frequency=440, duration=100):
        """비프음 생성"""
        return SoundEffects.create_tone(frequency, duration)

    @staticmethod
    def create_success_sound():
        """성공 음향 생성"""
        return SoundEffects.create_success_sound()

    @staticmethod
    def create_error_sound():
        """에러 음향 생성"""
        return SoundEffects.create_error_sound()


# 글로벌 사운드 매니저
_global_sound_manager = None


def get_sound_manager(volume=100, music_volume=80):
    """글로벌 사운드 매니저 가져오기"""
    global _global_sound_manager
    if _global_sound_manager is None:
        _global_sound_manager = SoundManager(volume, music_volume)
    return _global_sound_manager
