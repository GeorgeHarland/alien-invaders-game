'''
powerup.py
'''

import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    '''Class to handle the powerup'''

    def __init__(self,game):
        '''Initialize powerup system'''
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # Load image and set rect attribute
        self.image = pygame.image.load('images/powerup.bmp')
        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midtop

        # store positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        '''Move down the screen'''
        self.y += (self.settings.speedup_scale * 0.25)
        self.rect.y = self.y