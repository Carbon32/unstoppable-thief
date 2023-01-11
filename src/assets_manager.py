# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Assets Manager: 

class AssetsManager():
    def __init__(self, game):

        # Game:

        self.game = game

        # Camera:

        self.camera = {
            "Camera0" : self.game.load_game_image('assets/Camera/Camera_Left.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Camera1" : self.game.load_game_image('assets/Camera/Camera_Right.png', self.game.screen_width // 32, self.game.screen_width // 32),
        }

        # Items:

        self.items = {
            "Money" : self.game.load_game_image('assets/Money/Money.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "MoneyShining" : self.game.load_game_image('assets/Money/Money_Shining.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "UIMoney" : self.game.load_game_image('assets/Money/UIMoney.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Key" : self.game.load_game_image('assets/Key/Key.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "KeyShining" : self.game.load_game_image('assets/Key/Key_Shining.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "UIKey" : self.game.load_game_image('assets/Key/UIKey.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Safe" : self.game.load_game_image('assets/Safe/Safe.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SafeShining" : self.game.load_game_image('assets/Safe/Safe_Shining.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SafeOpen" : self.game.load_game_image('assets/Safe/Safe_Open.png', self.game.screen_width // 32, self.game.screen_width // 32)
        }

        # Walls:

        self.walls = {
            "Upper" : self.game.load_game_image('assets/Walls/Upper.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Lower" : self.game.load_game_image('assets/Walls/Lower.png', self.game.screen_width // 32, self.game.screen_width // 32)
        }

        # Buttons:

        self.buttons = {
            "MusicOn" : self.game.load_game_image('assets/Buttons/MusicOn.png', self.game.screen_width // 64, self.game.screen_width // 64),
            "MusicOff" : self.game.load_game_image('assets/Buttons/MusicOff.png', self.game.screen_width // 64, self.game.screen_width // 64),
            "SoundOn" : self.game.load_game_image('assets/Buttons/SoundOn.png', self.game.screen_width // 64, self.game.screen_width // 64),
            "SoundOff" : self.game.load_game_image('assets/Buttons/SoundOff.png', self.game.screen_width // 64, self.game.screen_width // 64)
        }