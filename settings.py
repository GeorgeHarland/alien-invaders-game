'''
settings.py
Stores all settings for Alien Invaders
GH
15/11/2021
'''

class Settings:
    '''A class to store all settings for the game'''
    
    def __init__(self):
        '''Initialize the game's static settings'''

        # Screen settings
        self.screen_width = 600
        self.screen_height = 900
        self.bg_color = (0,32,84)

        # Ship settings
        self.ship_lives = 3

        # Bullet settings
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (200,200,200)
        self.max_bullets = 4
        self.powerup_level = 0

        # Alien Settings
        self.vert_speed = 10

        # How quickly the game speeds up per wave
        self.speedup_scale = 1.2

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        '''Initialize settings that changed as the game progresses'''

        # Ship settings
        self.ship_speed = 0.4

        # Bullet settings
        self.bullet_speed = 0.75

        # Alien settings
        self.alien_speed = 0.2
        self.alien_points = 10

        # Here so aliens always move right with a new wave
        self.fleet_direction = 1 # 1 = right, -1 = left

    def increase_speed(self):
        '''Increase speed settings'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_speed += 0.05
        self.alien_points += 10