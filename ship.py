'''
ship.py
'''

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''A class to manage the ship'''
    def __init__(self, game):
        '''Initialize ship and set starting position'''
        super().__init__()

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # load ship image and get its rectangle
        self.image = pygame.image.load('images/playership.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal value for ships's positions + move the ship up slightly
        self.x = float(self.rect.x)
        self.y = float(self.rect.y) - 50

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ships position based on movement flags'''
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect based on changes make here
        self.rect.x = self.x
        self.rect.y = self.y
    
    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y) - 50