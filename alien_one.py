'''
alien_one.py
'''

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Represents a single alien'''

    def __init__(self, game):
        '''Initialize alien and set its starting position'''
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load alien image and set its rect attribute
        self.image = pygame.image.load('images/alienone.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store exact positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    
    def check_edges(self):
        '''Returns true if an alien hits the edge of the screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        '''Move the alien'''
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
