'''
alien_invaders.py
A space invaders-style game.
GH
15/11/2021
'''

import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from playbutton import Button
from score import Score
from powerup import PowerUp
from stars import StarDisplay
from ship import Ship
from bullet import Bullet
from alien_one import Alien

class AlienInvaders:
    '''Manages the game assets and behaviours.'''

    def __init__(self):
        '''Initialize the game and create game resources.'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
             (self.settings.screen_width, self.settings.screen_height))
        # For full screen (replace previous couple of lines):
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invaders')
        
        self.stats = GameStats(self)
        self.scoredisplay = Score(self)
        self.stardisplay = StarDisplay(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self._create_fleet()

        # Create the play button
        self.play_button = Button(self, "Start")

    def run_game(self):
        '''Starts the main loop of the game.'''

        # Create a new set of stars for the background
        self.stardisplay.get_random_stars()

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_powerups()

            self._update_screen()

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Start the game when the play button is clicked on'''
        if self.play_button.rect.collidepoint(mouse_pos):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                #Reset the game settings
                self.settings.init_dynamic_settings()
                self._start_game()

    def _start_game(self):
        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoredisplay.prep_score()
        self.scoredisplay.prep_level_count()
        self.scoredisplay.prep_ship_count()

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.powerups.empty()

        # Create a new set of stars for the background
        self.stardisplay.get_random_stars()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()


    def _create_fleet(self):
        '''Creates the fleet of aliens'''
        # Make an alien to start with
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaliable_space_x // (2 * alien_width)

        # Determine number of alien rows
        alien_rows = 4

        # Create full fleet
        for row_no in range(alien_rows):
            for a in range(number_aliens_x):
                self._create_alien(a, row_no)

    def _create_alien(self, alien_no, row_no):
        '''Creates a single alien and places it into the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_no
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 60 + 2 * alien.rect.height * row_no
        self.aliens.add(alien)

    def _create_powerup(self):
        '''Creates a single powerup'''
        powerup = PowerUp(self)
        powerup_width, powerup_height = powerup.rect.size
        powerup.x = powerup_width + 2 * powerup_width
        powerup.rect.x = powerup.x
        powerup.rect.y = powerup.rect.height + 60 + 2 * powerup.rect.height
        self.powerups.add(powerup)

    def _check_keydown(self, event):
        '''Respond to keys pressed'''
        if event.key == pygame.K_UP:
            # Flag the ship to move to up
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._player_shoot()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup(self,  event):
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _ship_hit(self):
        '''Respond to a collision between the player ship and an alien'''
        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1
            self.scoredisplay.prep_ship_count()

            # Get rid of any remaining sprites
            self.aliens.empty()
            self.bullets.empty()
            self.powerups.empty()

            # Create a new fleet and center the ship
            self.ship.center_ship()
            self._create_fleet()  

            # pause for a moment
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _player_shoot(self):
        '''Creates a new bullet object and adds it to the group of bullets'''
        #if self.settings.powerup_level == 1:
        if len(self.bullets) < self.settings.max_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        #elif self.settings.powerup_level == 2:
        #    if len(self.bullets) < self.settings.max_bullets:
        #        pass
                

    def _update_bullets(self):
        '''Updates the bullets on screen'''
        self.bullets.update()

        # Remove bullets that have gone off screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check if any bullets and aliens have collided & remove both if so
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # Update score when alien shot
        if collisions:
            for ali in collisions.values():
                self.stats.score += self.settings.alien_points * len(ali)
            self.scoredisplay.prep_score()
            self.scoredisplay.check_high_score()
            
        self._check_bullet_collisions()

    def _update_powerups(self):
        '''Updates the powerups on screen'''
        self.powerups.update()
        self._check_powerup_collisions()


    def _check_bullet_collisions(self): 
        '''Respond to collisions between bullets and aliens'''
        # Remove aliens that have gone off screen
        for a in self.aliens:
            if a.rect.bottom >= self.settings.screen_height:
                self.aliens.remove(a)
        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        # Destroy existing bullets and create new fleet
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level count
        self.stats.level += 1
        self.scoredisplay.prep_level_count()

        # Spawn a powerup at specific levels
        self._create_powerup()

    def _check_powerup_collisions(self):
        '''Look for powerup-ship collisions'''
        if pygame.sprite.spritecollideany(self.ship, self.powerups):
            self.settings.powerup_level += 1
            self._power_level_upgrade()
            # Allow powerup to be drawn over
            self.powerups.empty()

    def _power_level_upgrade(self):
        '''Upgrade stats based on what power level has been reached'''
        if self.settings.powerup_level == 1:
            self.settings.bullet_width = 6
        if self.settings.powerup_level == 2:
            self.settings.bullet_width = 20


    def _check_fleet_edges(self):
        '''Act if any aliens have hit the side of the screen'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        '''Drop down and change direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.vert_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if aliens hit the bottom
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        '''Check if the aliens have reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat as if ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        # Draw the screen
        self.stardisplay.prep_stars()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.powerups.draw(self.screen)

        # Draw score
        self.scoredisplay.show_score()

        # Draw play button if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recent screen drawn visible
        pygame.display.flip()

if __name__ == '__main__':
    # Create a game instance, then run the game
    ali = AlienInvaders()
    ali.run_game()