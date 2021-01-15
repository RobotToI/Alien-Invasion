import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for bulet managment, which ship spray"""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # Creating bulet in position (0,0) and giving the right position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Bulet position contains real format
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Moves bullet up to the screen top'''
        # Updating bullet position in real format
        self.y -= self.speed_factor
        # Updating rectangle position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Screen output of a bullet'''
        pygame.draw.rect(self.screen, self.color, self.rect)
