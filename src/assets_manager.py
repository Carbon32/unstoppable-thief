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
            "Play" : self.game.load_game_image('assets/Buttons/Play.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Editor" : self.game.load_game_image('assets/Buttons/Editor.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Exit" : self.game.load_game_image('assets/Buttons/Exit.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Again" : self.game.load_game_image('assets/Buttons/Again.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Select" : self.game.load_game_image('assets/Buttons/Select.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Save" : self.game.load_game_image('assets/Buttons/Save.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "Clear" : self.game.load_game_image('assets/Buttons/Clear.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "Back" : self.game.load_game_image('assets/Buttons/Back.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "MusicOn" : self.game.load_game_image('assets/Buttons/MusicOn.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "MusicOff" : self.game.load_game_image('assets/Buttons/MusicOff.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SoundOn" : self.game.load_game_image('assets/Buttons/SoundOn.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SoundOff" : self.game.load_game_image('assets/Buttons/SoundOff.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Lvl1" : self.game.load_game_image('assets/Buttons/Lvl_1.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl2" : self.game.load_game_image('assets/Buttons/Lvl_2.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl3" : self.game.load_game_image('assets/Buttons/Lvl_3.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl4" : self.game.load_game_image('assets/Buttons/Lvl_4.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl5" : self.game.load_game_image('assets/Buttons/Lvl_5.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl6" : self.game.load_game_image('assets/Buttons/Lvl_6.png', self.game.screen_width // 8, self.game.screen_width // 16)
        }