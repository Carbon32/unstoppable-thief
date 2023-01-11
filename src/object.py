# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Object: #

class Object(pygame.sprite.Sprite):
    def __init__(self, game, tile_size, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Game: 

        self.game = game

        # World: 

        self.tile_size = tile_size

        # Object Settings: 

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.tile_size // 2, y + (self.tile_size - self.image.get_height()))

    def draw(self):
        self.game.display.blit(self.image, self.rect)