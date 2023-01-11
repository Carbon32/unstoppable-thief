# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Sounds: #

class Sounds():
    def __init__(self, game):

        # Game:

        self.game = game

        # Music:

        self.music_status = True

        # Sounds: 

        self.sound_status = True

        # Available Sounds: 

        self.sounds = {
            'Footsteps' : self.game.load_game_sound('sounds/footsteps/footsteps.ogg'),
            'Door' : self.game.load_game_sound('sounds/door/door.ogg'),
            'Safe' : self.game.load_game_sound('sounds/crack/crack.ogg'),
            'Money' : self.game.load_game_sound('sounds/money/money.ogg'),
            'Key' : self.game.load_game_sound('sounds/key/key.ogg'),
            'Alarm' : self.game.load_game_sound('sounds/alarm/alarm.ogg')
        }

    def play_sound(self, sound : str, volume : float):
        if(self.sound_status):
            self.sounds[sound].set_volume(volume)
            pygame.mixer.Sound.play(self.sounds[sound])

    def stop_sound(self, sound : str):
        pygame.mixer.Sound.stop(self.sounds[sound])

    def play_music(self, music : str, volume : float):
        if(self.music_status):
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, 0.0, 5000)

    def stop_music(self):
        pygame.mixer.music.stop()

