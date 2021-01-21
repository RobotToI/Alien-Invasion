class GameStats():
    """Tracking stats for Alien Invasion """

    def __init__(self, ai_settings):
        '''Initialize a statistics'''
        self.ai_settings = ai_settings
        self.reset_status()
        self.get_high_score_from_file()
        # Game starts with non-active mode
        self.game_status = False

    def reset_status(self):
        '''Initialize statistics, that was changed by game procces'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score_from_file(self):
        '''We just return highest score frome file'''
            try:
                hs = open('record', 'r')
                self.high_score = int(hs.readline())
                hs.close()
            except:
                hs = open('record', 'r')
                self.high_score = 0
                hs.write('0')
                hs.close()

