'''
stars.py
'''

import pygame
import random

class StarDisplay:

    def __init__(self,game):
        '''...'''
        self.screen = game.screen
        self.settings = game.settings
        self.star_locations_x = []
        self.star_locations_y = []

    def prep_stars(self):
        ''' Create a new starry background'''
        self.screen.fill(self.settings.bg_color)
        for j in range(100):
            pygame.draw.circle(self.screen,(255,255,255),(self.star_locations_x[j],self.star_locations_y[j]),1)

    def get_random_stars(self):
        '''Get random locations for stars at the beginning of the game'''

        # Reset lists so changes every game
        self.star_locations_x = []
        self.star_locations_y = []

        # get random locations
        for i in range(100):
            self.star_locations_x.append(random.randint(1,self.settings.screen_width))
            self.star_locations_y.append(random.randint(1,self.settings.screen_height))

        # save in star_locations