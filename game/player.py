import pygame


class Puller:
    """Represents a puller character anchor on either side of the rope."""

    def __init__(self, x, y, color, label):
        self.x = x
        self.y = y
        self.color = color
        self.label = label
        self.font = pygame.font.SysFont(None, 24)

    def render(self, surface, pulling=False, direction=0):
        """Draw avatar and label."""

        # Small visual lean during a pull
        lean = direction * 8 if pulling else 0

        body_x = self.x + lean
        body_y = self.y

        # Body
        body_rect = pygame.Rect(
            body_x - 20,
            body_y - 35,
            40,
            70
        )

        pygame.draw.rect(
            surface,
            self.color,
            body_rect,
            border_radius=6
        )

        # Head
        pygame.draw.circle(
            surface,
            (240, 210, 180),
            (body_x, body_y - 50),
            16
        )

        # Name / control tag
        label_surf = self.font.render(
            self.label,
            True,
            (240, 240, 240)
        )

        surface.blit(
            label_surf,
            (
                self.x - label_surf.get_width() // 2,
                self.y + 45
            )
        )
