# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Key: #

class Key(pygame.sprite.Sprite):
    def __init__(self, game, tile_size, assets_manager, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Game: 

        self.game = game

        # Assets Manager:

        self.assets_manager = assets_manager

        # World: 

        self.tile_size = tile_size

        # Status:

        self.status = True

        # Image & Rectangle:

        self.image = self.assets_manager.items["Key"]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.tile_size // 2, y + (self.tile_size - self.image.get_height()))

    def draw(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        if(self.status):
            if(pygame.sprite.collide_rect(self, self.game.player)):
                self.image = self.assets_manager.items["KeyShining"]
                if(pygame.key.get_pressed()[pygame.K_f]):
                    self.image = self.assets_manager.walls["Upper"]
                    self.game.player.key = True
                    self.game.sounds.play_sound('Key', 0.1)
                    self.status = False

            else:
                self.image = self.assets_manager.items["Key"]
