# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon               		      #
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

	def draw_stats(self):
		if(self.game.player.money < 1000):
			self.game.draw_text(self.game.display, f'Money: ${self.game.player.money}', self.game.screen_width // 64, (255, 255, 255), self.game.screen_width // 32, (self.game.screen_height // 4 - self.game.screen_height // 4.4))
		else:
			self.game.draw_text(self.game.display, f'Money: ${self.game.player.money / 1000}K', self.game.screen_width // 64, (255, 255, 255), self.game.screen_width // 32, (self.game.screen_height // 4 - self.game.screen_height // 4.4))

		self.game.draw_text(self.game.display, f'Level: {self.game.level}', self.game.screen_width // 64, (255, 255, 255), self.game.screen_width // 4, (self.game.screen_height // 4 - self.game.screen_height // 4.4))
		self.game.draw_text(self.game.display, f'FPS: {int(self.game.fps_handler.get_fps())}', self.game.screen_width // 64, (255, 255, 255), self.game.screen_width // 2, (self.game.screen_height // 4 - self.game.screen_height // 4.4))
		self.game.draw_text(self.game.display, f'Time: {self.game.minutes[0]}{self.game.minutes[1]}:{self.game.seconds[0]}{self.game.seconds[1]}', self.game.screen_width // 64, (255, 255, 255), self.game.screen_width - (self.game.screen_width // 3), (self.game.screen_height // 4 - self.game.screen_height // 4.4))
		self.game.display.blit(self.assets_manager.items["UIMoney"], (0, (self.game.screen_height // 4 - self.game.screen_height // 3.85)))

		if(self.game.player.key):
			self.game.display.blit(self.assets_manager.items["UIKey"], (self.game.screen_width - (self.game.screen_width // 6), (self.game.screen_height // 4 - self.game.screen_height // 4)))