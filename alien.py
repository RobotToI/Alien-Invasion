import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class representing one alien"""

    def __init__(self, ai_settings, screen):
        '''Initialize alien and gives him a start position'''
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Loading an pic of alien and rect attr
        self.image = pygame. image.load('src/alien.bmp')
        self.rect = self.image.get_rect()

        # Every new alien appears in Up-Left corner of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Saving accurate position of an alien
        self.x = float(self.rect.x)

    def check_edges(self):
        '''Returns True, if alein is by the end of screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        '''Moves alien to the right and to the left'''
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        '''Ouput an alien in accurate position'''
        self.screen.blit(self.image, self.rect)
