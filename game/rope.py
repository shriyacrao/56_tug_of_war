import math
import pygame


class Rope:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_y = screen_height // 2
        self.marker_x = screen_width // 2

        self.left_win_x = 180
        self.right_win_x = screen_width - 180
        self.pull_step = 12

        # Visual-only tension
        self.tension = 0.0
        self.tension_time = 0.0

    def pull_left(self, strength=1.0):
        # Actual pulling mechanic stays unchanged
        self.marker_x -= int(self.pull_step * strength)

        # Visual tension only
        self.tension = min(1.0, self.tension + 0.25)
        self.tension_time += 0.8

    def pull_right(self, strength=1.0):
        # Actual pulling mechanic stays unchanged
        self.marker_x += int(self.pull_step * strength)

        # Visual tension only
        self.tension = min(1.0, self.tension + 0.25)
        self.tension_time += 0.8

    def check_winner(self):
        if self.marker_x <= self.left_win_x:
            return "PLAYER"

        if self.marker_x >= self.right_win_x:
            return "COMPUTER"

        return None

    def reset(self):
        self.marker_x = float(self.screen_width // 2)
        self.tension = 0.0
        self.tension_time = 0.0

    def update_visuals(self):
        # Slowly reduce visual tension between pulls
        self.tension = max(0.0, self.tension - 0.025)
        self.tension_time += 0.15

    def render(self, surface):
        start_x = 60
        end_x = self.screen_width - 60

        # Draw rope as connected segments so it can visibly move
        points = []
        segments = 30

        for i in range(segments + 1):
            t = i / segments

            x = start_x + (end_x - start_x) * t

            # Visual-only wave and sag
            wave_amplitude = 7 * self.tension
            sag = 5 * self.tension * math.sin(math.pi * t)

            wave = (
                wave_amplitude
                * math.sin(self.tension_time * 8 + t * math.pi * 5)
                * math.sin(math.pi * t)
            )

            y = self.center_y + sag + wave
            points.append((int(x), int(y)))

        if len(points) > 1:
            pygame.draw.lines(
                surface,
                (180, 140, 90),
                False,
                points,
                10
            )

        # Player win line
        pygame.draw.line(
            surface,
            (50, 200, 50),
            (self.left_win_x, self.center_y - 40),
            (self.left_win_x, self.center_y + 40),
            4
        )

        # Computer win line
        pygame.draw.line(
            surface,
            (200, 50, 50),
            (self.right_win_x, self.center_y - 40),
            (self.right_win_x, self.center_y + 40),
            4
        )

        # Center line
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (self.screen_width // 2, self.center_y - 20),
            (self.screen_width // 2, self.center_y + 20),
            2
        )

        # Marker / flag
        flag_rect = pygame.Rect(
            int(self.marker_x) - 12,
            self.center_y - 24,
            24,
            48
        )

        pygame.draw.rect(
            surface,
            (230, 40, 40),
            flag_rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            flag_rect,
            width=2,
            border_radius=4
        )
