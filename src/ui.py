# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# User Interface: #

class UserInterface():
    def __init__(self, game, assets_manager):
        
        # Game:

        self.game = game

        # Assets Manager:

        self.assets_manager = assets_manager
        
        # Container:

        self.container_color = (184, 160, 238)

    def draw_container(self):
        pygame.draw.rect(self.game.display, self.container_color, pygame.Rect(self.game.screen_width // (self.game.screen_width // 8), self.game.screen_height // 64, self.game.screen_width - (self.game.screen_width // (self.game.screen_width // 16)), self.game.screen_height // 10), border_radius = self.game.screen_width // 38)
        pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // (self.game.screen_width // 8), self.game.screen_height // 64,  self.game.screen_width - (self.game.screen_width // (self.game.screen_width // 16)), self.game.screen_height // 10), self.game.screen_width // 128, border_radius = self.game.screen_width // 38)
    
    def draw_stats(self):
        self.draw_container()
        if(self.game.player.money < 1000):
            self.game.draw_text(f'Money: ${self.game.player.money}', self.game.screen_width // 64, (48, 45, 45), self.game.screen_width // 16, self.game.screen_height // 18)
        else:
            self.game.draw_text(f'Money: ${self.game.player.money / 1000}K', self.game.screen_width // 64, (48, 45, 45), self.game.screen_width // 16, self.game.screen_height // 18)
        self.game.draw_text(f'Level: {self.game.level}', self.game.screen_width // 64, (48, 45, 45), self.game.screen_width // 4, self.game.screen_height // 18)
        self.game.draw_text(f'FPS: {int(self.game.fps_handler.get_fps())}', self.game.screen_width // 64, (48, 45, 45), self.game.screen_width // 2, self.game.screen_height // 18)
        self.game.draw_text(f'Time: {self.game.minutes[0]}{self.game.minutes[1]}:{self.game.seconds[0]}{self.game.seconds[1]}', self.game.screen_width // 64, (48, 45, 45), self.game.screen_width - (self.game.screen_width // 3), self.game.screen_height // 18)
        self.game.display.blit(self.assets_manager.items["UIMoney"], (self.game.screen_width // 32, (self.game.screen_height // 4 - self.game.screen_height // 4.4)))
        if(self.game.player.key):
            self.game.display.blit(self.assets_manager.items["UIKey"], (self.game.screen_width - (self.game.screen_width // 6), (self.game.screen_height // 4 - self.game.screen_height // 4.6)))