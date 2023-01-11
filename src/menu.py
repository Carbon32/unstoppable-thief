# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu:

class Menu():
    def __init__(self, game, world, assets_manager):

        # Game:

        self.game = game

        # World:

        self.world = world

        # Assets Manager:

        self.assets_manager = assets_manager

        #  Menu Settings: 

        self.main_menu = True

        # Level Selector:

        self.selected_level = 0

        # Level Designs:

        self.level_designs = []
        for i in range(len(os.listdir('assets/Levels/'))):
            self.level_designs.append(self.game.load_game_image(f'assets/Levels/Level{i}.png', self.game.screen_width // 2, self.game.screen_height // 2))

        # Border:

        self.border = pygame.Rect(0, 0, 0, 0)

        # Buttons:

        self.play_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 3), self.assets_manager.buttons["Play"])
        self.again_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 3), self.assets_manager.buttons["Again"])
        self.editor_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 6), self.assets_manager.buttons["Editor"])
        self.exit_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 6 + (self.game.screen_height // 3), self.assets_manager.buttons["Exit"])
        self.select_button = Button(self.game.display, self.game.screen_width // 4 + (self.game.screen_width // 4), self.game.screen_height // 2 + (self.game.screen_height // 4), self.assets_manager.buttons["Select"])
        self.music_button = Button(self.game.display, self.game.screen_width // 2 + (self.game.screen_width // 2.3), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.assets_manager.buttons["MusicOn"])
        self.sound_button = Button(self.game.display, self.game.screen_width // 2 + (self.game.screen_width // 2.8), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.assets_manager.buttons["SoundOn"])
        self.back_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 6 + (self.game.screen_height // 2), self.assets_manager.buttons["Back"])
        self.level1 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 4), self.assets_manager.buttons["Lvl1"])
        self.level2 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 6), self.assets_manager.buttons["Lvl2"])
        self.level3 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 12), self.assets_manager.buttons["Lvl3"])
        
    def handle_menu(self):
        if(self.game.menu_on):
            self.game.set_background((185, 189, 193))
            if(self.main_menu or self.game.game_ready):
                if(self.game.game_ready):
                    if(self.back_button.render()):
                        self.main_menu = False
                        self.game.menu_on = False
                        self.game.music_started = False

                if(self.play_button.render()):
                    if(self.game.game_ready):
                        self.main_menu = False
                        self.game.level_selector = True
                        self.game.game_ready = False
                    else:
                        self.main_menu = False

                if(self.editor_button.render()):
                    self.world.set_game_level(self.game.level)
                    self.game.level_selector = False
                    self.game.editor_status = True
                    self.game.menu_on = False
                    self.game.game_ready = False
                    self.main_menu = False

                if(self.music_button.render()):
                    if(self.game.sounds.music_status):
                        self.music_button.change_button(self.assets_manager.buttons["MusicOff"])
                        self.game.sounds.music_status = False
                        self.game.sounds.stop_music()
                    else:
                        self.music_button.change_button(self.assets_manager.buttons["MusicOn"])
                        self.game.sounds.music_status = True
                        self.game.music_started = False

                if(self.sound_button.render()):
                    if(self.game.sounds.sound_status):
                        self.sound_button.change_button(self.assets_manager.buttons["SoundOff"])
                        self.game.sounds.sound_status = False
                    else:
                        self.sound_button.change_button(self.assets_manager.buttons["SoundOn"])
                        self.game.sounds.sound_status = True

                if(self.exit_button.render()):
                    self.game.engine_running = False
            else:

                if(self.game.level_selector):
                    if(self.level1.render()):
                        self.selected_level = 1
                        self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 4), self.game.screen_width // 8, self.game.screen_width // 16)

                    if(self.level2.render()):
                        self.selected_level = 2
                        self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 6), self.game.screen_width // 8, self.game.screen_width // 16)

                    if(self.level3.render()):
                        self.selected_level = 3
                        self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 12), self.game.screen_width // 8, self.game.screen_width // 16)

                    if(self.select_button.render() and self.selected_level != 0):
                        self.world.set_game_level(self.selected_level)
                        self.game.level_selector = False
                        self.game.menu_on = False
                        self.game.music_started = False

                if(self.selected_level > len(self.level_designs) - 1):
                    self.game.display.blit(self.level_designs[0], (self.game.screen_width // 3, self.game.screen_height // 6))
                else:
                    self.game.display.blit(self.level_designs[self.selected_level], (self.game.screen_width // 3, self.game.screen_height // 6))

                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3, self.game.screen_height // 6, self.game.screen_width // 2, self.game.screen_height // 2), self.game.screen_width // 128)
                pygame.draw.rect(self.game.display, (150, 255, 0), self.border, self.game.screen_width // 128)

    def check_for_arrest(self):
        if(not self.game.state):
            if(self.again_button.render()):
                self.game.sounds.stop_sound('Alarm')
                self.game.music_started = False
                self.world.set_game_level(self.game.level)
                self.game.player.key = False
                self.game.player.money = 0
                self.game.state = True
                self.game.minutes = [0, 0]
                self.game.seconds = [0, 0]