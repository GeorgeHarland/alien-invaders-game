'''
score.py
'''

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Score:
    '''Displays score on screen'''

    def __init__(self,game):
        '''Initialize score attributes'''
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        # Font settings
        self.score_color = (255,255,255)
        self.hs_color = (255,255,0)
        self.font = pygame.font.SysFont(None,36)

        # Prep
        self.prep_score()
        self.prep_high_score()
        self.prep_level_count()
        self.prep_ship_count()

    def prep_score(self):
        '''Turns score into image to display'''
        score_str = 'Score: ' + str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                self.score_color, self.settings.bg_color)

        # Display at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # Laid out as if need to round
        high_score = round(self.stats.high_score, -1)
        high_score_str = '  High Score: ' + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.hs_color, self.settings.bg_color)

        # Center high score at topleft of screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.topleft = self.screen_rect.topleft
        self.high_score_rect.top = self.score_rect.top

    def prep_level_count(self):
        '''Turns level count into an image'''
        level_str = 'Level: ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.score_color, self.settings.bg_color)

        # Position below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ship_count(self):
        '''Show how many lives are lefts'''
        self.ships = Group()
        for ship_no in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_no * ship.rect.width
            ship.rect.y = self.settings.screen_height-50
            self.ships.add(ship)

    def show_score(self):
        '''Draw all to screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        '''Check to see if new high score reached'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()