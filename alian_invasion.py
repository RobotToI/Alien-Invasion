import pygame
from ship import Ship
from alien import Alien
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from pygame.sprite import Group
import game_functions as gf
'''This is start structure of alian_invasion'''


def run_game():
    # Initialazing pygame, settings and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption('Alian Invasion')
    play_button = Button(ai_settings, screen, "Play")
    # Creation GameStats and Score a object
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Creation ship object
    ship = Ship(ai_settings, screen)
    # Creation alien object
    # alien = Alien(ai_settings, screen)
    # Creation groupe of bullets
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Main loop game start
    while True:
        # Check statement of keyboard and mouse
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_status:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                              aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen,
                             sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


def main():
    run_game()


if __name__ == '__main__':
    main()
