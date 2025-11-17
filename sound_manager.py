#!/usr/bin/env python3
"""
사운드 및 음악 관리 시스템
"""
import pygame
from pathlib import Path
import os

class SoundManager:
    """사운드 및 음악 관리"""

    def __init__(self, volume=100, music_volume=80):
        self.volume = volume
        self.music_volume = music_volume
        self.sounds = {}
        self.current_music = None
        self.music_playing = False

        # Pygame mixer 초기화
        try:
            pygame.mixer.init()
        except:
            self.enabled = False
            return

        self.enabled = True

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

    def play_sound(self, name):
        """사운드 재생"""
        if not self.enabled or name not in self.sounds:
            return

        try:
            self.sounds[name].play()
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

    def play_music(self, loops=-1):
        """음악 재생"""
        if not self.enabled or not self.current_music:
            return

        try:
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except:
            pass

    def stop_music(self):
        """음악 중지"""
        if not self.enabled:
            return

        try:
            pygame.mixer.music.stop()
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


# 기본 사운드 효과
class DefaultSounds:
    """기본 사운드 이펙트 생성"""

    @staticmethod
    def create_beep(frequency=440, duration=100):
        """비프음 생성"""
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
        """성공 음향 생성"""
        # 두 개의 비프음 조합
        if not pygame.mixer.get_init():
            return None

        try:
            sound1 = DefaultSounds.create_beep(523, 100)  # C5
            if sound1:
                return sound1
        except:
            pass
        return None

    @staticmethod
    def create_error_sound():
        """에러 음향 생성"""
        if not pygame.mixer.get_init():
            return None

        try:
            sound = DefaultSounds.create_beep(220, 200)  # A3
            return sound
        except:
            pass
        return None


# 글로벌 사운드 매니저
_global_sound_manager = None


def get_sound_manager(volume=100, music_volume=80):
    """글로벌 사운드 매니저 가져오기"""
    global _global_sound_manager
    if _global_sound_manager is None:
        _global_sound_manager = SoundManager(volume, music_volume)
    return _global_sound_manager
