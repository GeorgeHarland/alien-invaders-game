'''
bullet.py
'''

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''A class to manage bullets fired from the player ship'''

    def __init__(self, game):
        '''Create a bullet object at the player ship's position'''
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0)
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,
            self.settings.bullet_height)

        # Set position of bullets
        self.rect.midtop = game.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        '''Moves the bullet up the screen'''
        # Update the position of bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draws the bullet onto the screen'''
        pygame.draw.rect(self.screen,self.color,self.rect)