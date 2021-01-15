import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ship, stats, ai_settings, screen, bullets):
    '''Reacting on key pushing'''
    if event.key == pygame.K_RIGHT:
        # Move our ship right
        ship.moving_right = True
    elif event.key == pygame.K_q:
        write_to_file(stats)
        sys.exit()
    elif event.key == pygame.K_LEFT:
        # Move our ship left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create new bullet and include this into group of bullets
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire bullet if max is not reached'''
    # Create new bullet and include this into group of bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    '''Reacting on key pushing stop'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship,
                 aliens, bullets):
    """Check keys pushing and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            write_to_file(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, stats,
                                 ai_settings, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    '''Starts new game while button Play is pressed'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_status:
        # Reset game statistics
        stats.reset_status()
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_status = True
        # Cleaning stats and score parametrs
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Cleaning alien and bullet list
        aliens.empty()
        bullets.empty()

        # Creating new fleet and placing ship into center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_fleet_edges(ai_settings, aliens):
    '''React on touch the edge screen by the alien'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_high_score(stats, sb):
    '''This function chekes does new record exist'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship,
                                 aliens, bullets):
    '''Treatment collision between bullets and aliens'''
    # Destruction of bullets and aliens, which was in collision
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        stats.score += ai_settings.alien_points
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destruction existing bullets and creation new fleet
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Checks, are aliens touch the bottom edge of screen'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # The same action as alien and ship collision
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Downs all the fleet and changes fleet direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settings, alien_width):
    '''Culculate how much aliens in a row'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Defines number of rows, which can be dwew on a screen'''
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    return int(available_space_y / (2 * alien_height))


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Prosses collision between ship and alien ship'''
    if stats.ships_left > 1:
        # ships_left -1
        stats.ships_left -= 1
        sb.prep_ships()
        # Cleaning lists of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Creaition new fleet and placing ship onto center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause the game
        sleep(0.5)
    else:
        stats.game_status = False
        pygame.mouse.set_visible(True)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Creating an alien and puts him in a row'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''Create fleet of aliens'''
    # Creation alien and canculation how much aliens in one row
    # Interval between neighbour aliens = one width of alien

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    del alien

    # Creation a first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Creation of an alien and placing him in a row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''Updates positions of all the aliens in out fleet'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # Collision check 'ship - alien'
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_bullets(ai_settings, screen, stats, sb, ship,
                   aliens, bullets):
    '''Updates bullet position and delete old bullets out of the screen'''
    # Updating bullets position
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Checking hits in aliens
    # If have a collision delete the alien and the bullet
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship,
                                 aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    '''Updates pictures on your screen and shows new screen pic'''
    # Кнопка Play отображается в том случае, если игра неактивна.
    # For every iteration redraw screen
    screen.fill(ai_settings.bg_color)
    # For all bullets prints on back of alians and ship
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    if stats.game_status:
        aliens.draw(screen)
        sb.show_score()
    if not stats.game_status:
        play_button.draw_button()
    # Show last drew screen
    pygame.display.flip()


def write_to_file(stats):
    with open('record', 'w') as hs:
        hs.write(str(stats.high_score))
