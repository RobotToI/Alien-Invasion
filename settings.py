# This file include different settings value


class Settings():
    """Class for saving all the game settings"""

    def __init__(self):
        ''' Initialazing static game settings'''
        # Start parametrs of a screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (35, 84, 103)
        # Start parametrs of a ship
        self.ship_limit = 3
        self.fleet_drop_speed = 5
        # Speed of game
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # Start parametrs of a bulet
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

    def initialize_dynamic_settings(self):
        '''Initializing of settings, which chage by the game flow'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 25
        # fleet_direction = 1 is right moving; a-1 is left moving
        self.fleet_direction = 1  # Moving to the right

    def increase_speed(self):
        '''Multiply speed settings'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
