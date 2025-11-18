#!/usr/bin/env python3
"""
리더보드 UI 시스템
- 게임 리더보드 표시
- 통계 시각화
- 성과 표시
"""
import pygame
from graphics_themes import Color, Themes
from statistics_manager import get_statistics_manager
from achievement_system import get_achievement_manager


class LeaderboardUI:
    """리더보드 UI"""

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.theme = Themes.NEON

        self.stats_manager = get_statistics_manager()
        self.achievement_manager = get_achievement_manager()

        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Statistics & Leaderboard")

        self.clock = pygame.time.Clock()
        self.running = True

    def draw_leaderboard(self, surface, leaderboard: list, title: str,
                        y_offset: int = 50):
        """리더보드 그리기"""
        font_title = pygame.font.Font(None, 40)
        font_header = pygame.font.Font(None, 28)
        font_row = pygame.font.Font(None, 24)

        # 제목
        title_text = font_title.render(title, True, self.theme.primary_color)
        surface.blit(title_text, (50, y_offset))

        # 헤더
        header_y = y_offset + 50
        rank_text = font_header.render("순위", True, self.theme.secondary_color)
        name_text = font_header.render("게임명", True, self.theme.secondary_color)
        score_text = font_header.render("점수", True, self.theme.secondary_color)

        surface.blit(rank_text, (50, header_y))
        surface.blit(name_text, (120, header_y))
        surface.blit(score_text, (450, header_y))

        # 구분선
        pygame.draw.line(surface, self.theme.secondary_color,
                        (50, header_y + 35), (750, header_y + 35), 2)

        # 리더보드 항목
        for i, (rank, name, score) in enumerate(leaderboard):
            row_y = header_y + 50 + (i * 35)

            rank_str = f"#{rank}"
            rank_surface = font_row.render(rank_str, True, Color.YELLOW)
            name_surface = font_row.render(name[:20], True, self.theme.primary_color)
            score_surface = font_row.render(str(score), True, self.theme.primary_color)

            surface.blit(rank_surface, (50, row_y))
            surface.blit(name_surface, (120, row_y))
            surface.blit(score_surface, (450, row_y))

    def draw_statistics_summary(self, surface):
        """통계 요약 그리기"""
        font_title = pygame.font.Font(None, 40)
        font_normal = pygame.font.Font(None, 28)

        stats = self.stats_manager.get_global_statistics()

        title = font_title.render("전체 통계", True, self.theme.primary_color)
        surface.blit(title, (50, 50))

        stat_lines = [
            f"총 게임 수: {stats['total_games']}",
            f"총 승리: {stats['total_wins']}",
            f"총 패배: {stats['total_losses']}",
            f"승률: {stats['win_rate']:.1f}%",
            f"총 점수: {stats['total_score']:,}",
            f"평균 점수: {stats['average_score']:,}",
            f"총 플레이 시간: {stats['total_hours']:.1f}시간"
        ]

        y_pos = 120
        for line in stat_lines:
            text = font_normal.render(line, True, self.theme.primary_color)
            surface.blit(text, (100, y_pos))
            y_pos += 45

    def draw_achievements(self, surface):
        """성과 표시"""
        font_title = pygame.font.Font(None, 40)
        font_normal = pygame.font.Font(None, 24)

        summary = self.achievement_manager.get_summary()
        badges = self.achievement_manager.get_unlocked_badges()

        # 제목
        title = font_title.render(
            f"성과 ({summary['unlocked_badges']}/{summary['total_badges']})",
            True, self.theme.primary_color
        )
        surface.blit(title, (50, 50))

        # 진행률 바
        progress_bar_width = 600
        progress_bar_height = 30
        progress_percent = summary['progress_percent'] / 100

        pygame.draw.rect(surface, Color.DARK_GRAY,
                        (50, 120, progress_bar_width, progress_bar_height))
        pygame.draw.rect(surface, Color.GREEN,
                        (50, 120, int(progress_bar_width * progress_percent),
                         progress_bar_height))
        pygame.draw.rect(surface, self.theme.primary_color,
                        (50, 120, progress_bar_width, progress_bar_height), 2)

        # 진행률 텍스트
        progress_text = font_normal.render(
            f"{summary['progress_percent']:.1f}%",
            True, Color.WHITE
        )
        surface.blit(progress_text, (300, 125))

        # 획득한 뱃지
        y_pos = 180
        for i, badge in enumerate(badges[:8]):  # 최대 8개 표시
            col = i % 4
            row = i // 4
            x_pos = 100 + col * 150
            y_pos_badge = y_pos + row * 100

            # 뱃지 아이콘
            icon_text = font_title.render(badge.icon, True, Color.YELLOW)
            surface.blit(icon_text, (x_pos, y_pos_badge))

            # 뱃지 이름
            name_text = font_normal.render(badge.name, True, self.theme.primary_color)
            surface.blit(name_text, (x_pos - 20, y_pos_badge + 40))

    def draw_game_rankings(self, surface):
        """게임별 순위 표시"""
        font_title = pygame.font.Font(None, 40)
        font_header = pygame.font.Font(None, 24)
        font_row = pygame.font.Font(None, 20)

        title = font_title.render("상위 게임 (최고 점수)", True, self.theme.primary_color)
        surface.blit(title, (50, 50))

        leaderboard = self.stats_manager.get_top_games(10)

        header_y = 110
        name_text = font_header.render("게임", True, self.theme.secondary_color)
        score_text = font_header.render("최고 점수", True, self.theme.secondary_color)

        surface.blit(name_text, (60, header_y))
        surface.blit(score_text, (400, header_y))

        # 구분선
        pygame.draw.line(surface, self.theme.secondary_color,
                        (50, header_y + 30), (750, header_y + 30), 1)

        # 항목
        for i, (rank, name, score) in enumerate(leaderboard):
            row_y = header_y + 45 + (i * 30)

            rank_str = f"#{rank}"
            rank_text = font_row.render(rank_str, True, Color.YELLOW)
            name_surface = font_row.render(name[:30], True, self.theme.primary_color)
            score_surface = font_row.render(str(score), True, Color.GREEN)

            surface.blit(rank_text, (60, row_y))
            surface.blit(name_surface, (100, row_y))
            surface.blit(score_surface, (400, row_y))

    def show_main_menu(self):
        """메인 메뉴 표시"""
        font = pygame.font.Font(None, 40)

        options = [
            "1: 전체 통계",
            "2: 상위 게임",
            "3: 성과/뱃지",
            "4: 게임별 순위",
            "5: 통계 내보내기",
            "ESC: 종료"
        ]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_1:
                        self.show_global_statistics()
                    elif event.key == pygame.K_2:
                        self.show_top_games()
                    elif event.key == pygame.K_3:
                        self.show_achievements()
                    elif event.key == pygame.K_4:
                        self.show_game_rankings()
                    elif event.key == pygame.K_5:
                        self.stats_manager.export_statistics()
                        print("통계를 내보냈습니다!")

            self.display.fill(self.theme.bg_color)

            # 제목
            title_text = font.render("Game Statistics & Leaderboard", True,
                                    self.theme.primary_color)
            self.display.blit(title_text, (150, 100))

            # 메뉴 옵션
            y_pos = 250
            for option in options:
                option_text = font.render(option, True, self.theme.primary_color)
                self.display.blit(option_text, (200, y_pos))
                y_pos += 60

            pygame.display.flip()
            self.clock.tick(60)

    def show_global_statistics(self):
        """전체 통계 표시"""
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False

            self.display.fill(self.theme.bg_color)
            self.draw_statistics_summary(self.display)

            # 돌아가기 안내
            font_small = pygame.font.Font(None, 24)
            back_text = font_small.render("ESC를 눌러 돌아가기", True,
                                         self.theme.secondary_color)
            self.display.blit(back_text, (50, 550))

            pygame.display.flip()
            self.clock.tick(60)

    def show_top_games(self):
        """상위 게임 표시"""
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False

            self.display.fill(self.theme.bg_color)
            self.draw_game_rankings(self.display)

            # 돌아가기 안내
            font_small = pygame.font.Font(None, 24)
            back_text = font_small.render("ESC를 눌러 돌아가기", True,
                                         self.theme.secondary_color)
            self.display.blit(back_text, (50, 550))

            pygame.display.flip()
            self.clock.tick(60)

    def show_achievements(self):
        """성과 표시"""
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False

            self.display.fill(self.theme.bg_color)
            self.draw_achievements(self.display)

            # 돌아가기 안내
            font_small = pygame.font.Font(None, 24)
            back_text = font_small.render("ESC를 눌러 돌아가기", True,
                                         self.theme.secondary_color)
            self.display.blit(back_text, (50, 550))

            pygame.display.flip()
            self.clock.tick(60)

    def show_game_rankings(self):
        """게임 순위 표시"""
        waiting = True
        while waiting and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False

            self.display.fill(self.theme.bg_color)
            self.draw_game_rankings(self.display)

            # 돌아가기 안내
            font_small = pygame.font.Font(None, 24)
            back_text = font_small.render("ESC를 눌러 돌아가기", True,
                                         self.theme.secondary_color)
            self.display.blit(back_text, (50, 550))

            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        """실행"""
        pygame.init()
        self.show_main_menu()
        pygame.quit()


if __name__ == "__main__":
    ui = LeaderboardUI()
    ui.run()
