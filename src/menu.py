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

        self.play_button = ButtonText(self.game, 'Play', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 2 - (self.game.screen_height // 6), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.editor_button = ButtonText(self.game, 'Editor', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 3 + (self.game.screen_height // 5), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.exit_button = ButtonText(self.game, 'Exit', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 3 + (self.game.screen_height // 2.5), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.again_button = ButtonText(self.game, 'Again', self.game.screen_width // 2 - (self.game.screen_width // 16), self.game.screen_height // 2 - (self.game.screen_height // 4), self.game.screen_width // 6, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.select_button = ButtonText(self.game, 'Select', self.game.screen_width // 4 + (self.game.screen_width // 4), self.game.screen_height // 2 + (self.game.screen_height // 4), self.game.screen_width // 6, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.back_button = ButtonText(self.game, 'Back', self.game.screen_width // 2 - (self.game.screen_width // 64),  self.game.screen_height // 2.9 + (self.game.screen_height // 1.8), self.game.screen_width // 14, self.game.screen_width // 20, self.game.screen_width // 256, 'small')
        self.music_button = ButtonImage(self.game.display, self.assets_manager.buttons["MusicOn"], self.game.screen_width // 2 + (self.game.screen_width // 2.3), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.game.screen_width // 32, self.game.screen_width // 32, self.game.screen_width // 256, self.game.screen_width // 64)
        self.sound_button = ButtonImage(self.game.display, self.assets_manager.buttons["SoundOn"], self.game.screen_width // 2 + (self.game.screen_width // 2.8), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.game.screen_width // 32, self.game.screen_width // 32, self.game.screen_width // 256, self.game.screen_width // 64)

        # Levels: 

        self.levels = {
            '1' : ButtonText(self.game, 'Level 1', self.game.screen_width // 24, self.game.screen_height // 2 - (self.game.screen_width // 4), self.game.screen_width // 4, self.game.screen_width // 16, self.game.screen_width // 80, 'large'),
            '2' : ButtonText(self.game, 'Level 2', self.game.screen_width // 24, self.game.screen_height // 2 - (self.game.screen_width // 6), self.game.screen_width // 4, self.game.screen_width // 16, self.game.screen_width // 80, 'large'),
            '3' : ButtonText(self.game, 'Level 3', self.game.screen_width // 24, self.game.screen_height // 2 - (self.game.screen_width // 12), self.game.screen_width // 4, self.game.screen_width // 16, self.game.screen_width // 80, 'large'),
        }

        # Title:

        self.step = 0
        self.title_background_color = (184, 160, 238)

    def handle_menu(self):
        if(self.game.menu_on):
            self.game.set_background((40, 42, 53))
            if(self.main_menu or self.game.game_ready):
                bounce = -1 * math.sin(self.step) * self.game.screen_width // 64
                pygame.draw.rect(self.game.display, self.title_background_color, pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), border_radius = self.game.screen_width // 38)
                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), self.game.screen_width // 128, border_radius = self.game.screen_width // 38)
                self.game.draw_custom_text(self.game.fonts['large'], 'Unstoppable Thief', (0, 0, 0), self.game.screen_width // 3.2, (0 + self.game.screen_height // 10) + bounce)
                self.step += 0.05
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
                    if(self.levels['1'].render()):
                        self.selected_level = 1

                    if(self.levels['2'].render()):
                        self.selected_level = 2

                    if(self.levels['3'].render()):
                        self.selected_level = 3

                    if(self.select_button.render() and self.selected_level != 0):
                        self.world.set_game_level(self.selected_level)
                        self.game.level_selector = False
                        self.game.menu_on = False
                        self.game.music_started = False

                if(self.selected_level > len(self.level_designs) - 1):
                    self.game.display.blit(self.level_designs[0], (self.game.screen_width // 3, self.game.screen_height // 6))
                else:
                    self.game.display.blit(self.level_designs[self.selected_level], (self.game.screen_width // 3, self.game.screen_height // 6))

                if(self.selected_level != 0):
                    self.levels[str(self.selected_level)].change_color((120, 212, 100), (71, 187, 100))

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