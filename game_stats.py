'''
game_stats.py
'''

class GameStats:
    '''Tracks statistics for Alien Invaders'''
    
    def __init__(self, game):
        '''Initialize stats system'''
        self.settings = game.settings
        self.reset_stats()

        # Flags the game to not run yet
        self.game_active = False

        # Stats that do not changed after the game is restarted
        self.high_score = 0

    def reset_stats(self):
        '''Initialize stats'''
        self.ships_left = self.settings.ship_lives
        self.score = 0
        self.level = 1