import random
import pygame
from game.rope import Rope
from game.player import Puller


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rope = Rope(width, height)
        self.player = Puller(90, height // 2, (50, 120, 220), "PLAYER (A/D)")
        self.computer = Puller(width - 90, height // 2, (220, 80, 50), "COMPUTER")

        self.last_key = None
        self.winner = None
        self.game_state = "PLAYING"
        
        # Match timer
        self.match_duration = 45000
        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False
        
        self.computer_pull_cooldown = 180
        self.last_computer_pull = pygame.time.get_ticks()
        
        self.player_pull_until = 0
        self.computer_pull_until = 0
        
        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 26)

    def handle_event(self, event):
        if self.game_state != "PLAYING":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_d):
                if event.key != self.last_key:
                    pull_strength = 2.0 if self.sudden_death else 1.0

                    self.rope.pull_left(pull_strength)
                    self.last_key = event.key

                    # Start short player pull animation
                    self.player_pull_until = pygame.time.get_ticks() + 140
        
    def update(self):
        if self.game_state != "PLAYING":
            return

        now = pygame.time.get_ticks()

        # Update rope visuals only
        self.rope.update_visuals()

        # Check match timer
        if not self.sudden_death:
            elapsed = now - self.match_start_time

            if elapsed >= self.match_duration:
                self.sudden_death = True

        distance_to_player_goal = self.rope.marker_x - self.rope.left_win_x

        if distance_to_player_goal <= 150:
            computer_cooldown = 100
            panic_multiplier = 1.4
        else:
            computer_cooldown = self.computer_pull_cooldown
            panic_multiplier = 1.0

        if now - self.last_computer_pull >= computer_cooldown:
            computer_variance = random.uniform(0.7, 1.2)
            computer_variance *= panic_multiplier

            # Double computer pull during Sudden Death
            if self.sudden_death:
                computer_variance *= 2.0

            self.rope.pull_right(computer_variance)
            self.last_computer_pull = now

            # Start short computer pull animation
            self.computer_pull_until = now + 140

        result = self.rope.check_winner()

        if result:
            self.winner = result
            self.game_state = "GAME_OVER"
            
    def reset(self):
        self.rope.reset()
        self.last_key = None
        self.player_pull_until = 0
        self.computer_pull_until = 0

        self.winner = None
        self.game_state = "PLAYING"

        self.match_start_time = pygame.time.get_ticks()
        self.sudden_death = False

        self.last_computer_pull = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((30, 32, 36))
        now = pygame.time.get_ticks()

        if self.sudden_death:
            timer_text = "SUDDEN DEATH"
        else:
            remaining = max(
                0,
                (self.match_duration - (now - self.match_start_time) + 999) // 1000
            )
            timer_text = f"Time: {remaining}s"

        timer_surf = self.font_small.render(
            timer_text,
            True,
            (240, 240, 240)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2 - timer_surf.get_width() // 2,
                10
            )
        )
        mud_rect = pygame.Rect(self.width // 2 - 120, self.height // 2 - 80, 240, 160)
        pygame.draw.rect(screen, (45, 38, 30), mud_rect, border_radius=12)

        self.rope.render(screen)
        now = pygame.time.get_ticks()

        player_pulling = now < self.player_pull_until
        computer_pulling = now < self.computer_pull_until

        self.player.render(
            screen,
            pulling=player_pulling,
            direction=-1
        )

        self.computer.render(
            screen,
            pulling=computer_pulling,
            direction=1
        )

        inst_surf = self.font_small.render(
            "Alternate [A] and [D] keys rapidly to pull!", True, (210, 210, 210)
        )
        screen.blit(inst_surf, (self.width // 2 - inst_surf.get_width() // 2, 40))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            win_text = f"{self.winner} WINS!"
            color = (80, 220, 80) if self.winner == "PLAYER" else (240, 80, 80)
            text_surf = self.font_big.render(win_text, True, color)
            screen.blit(
                text_surf,
                (self.width // 2 - text_surf.get_width() // 2, self.height // 2 - 50)
            )

            restart_surf = self.font_small.render(
                "Press [R] to Play Again", True, (240, 240, 240)
            )
            screen.blit(
                restart_surf,
                (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 10)
            )
