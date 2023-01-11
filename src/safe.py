# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Safe: #

class Safe(pygame.sprite.Sprite):
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

        self.image = self.assets_manager.items["Safe"]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.tile_size // 2, y + (self.tile_size - self.image.get_height()))

        # Timers:

        self.current_time = pygame.time.get_ticks()
        self.cracking_time = 25

    def draw(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        if(self.status):
            if(pygame.sprite.collide_rect(self, self.game.player)):
                self.image = self.assets_manager.items["SafeShining"]
                if(not self.game.player.interacting):
                    if(pygame.key.get_pressed()[pygame.K_f]):
                        self.game.sounds.play_sound('Safe', 0.1)
                        self.game.player.interacting = True
            else:
                self.image = self.assets_manager.items["Safe"]

        if(self.game.player.interacting):
            pygame.draw.rect(self.game.display, (90, 144, 255), (self.game.player.rect.x - self.game.player.rect.w // 2, self.game.player.rect.top - self.game.player.rect.h // 2.8, (self.rect.w), self.game.screen_width // 256))
            pygame.draw.rect(self.game.display, (255, 40, 80), (self.game.player.rect.x - self.game.player.rect.w // 2, self.game.player.rect.top - self.game.player.rect.h // 2.8, (self.rect.w) * (self.game.progress / 100), self.game.screen_width // 256))
            pygame.draw.rect(self.game.display, (255, 255, 255), (self.game.player.rect.x - self.game.player.rect.w // 2, self.game.player.rect.top - self.game.player.rect.h // 2.8,(self.rect.w), self.game.screen_width // 256), 2)
            if(self.game.progress < 100):
                if(pygame.time.get_ticks() - self.current_time > self.cracking_time):
                    self.game.progress += 1
                    self.current_time = pygame.time.get_ticks()
            else:
                self.image = self.assets_manager.items["SafeOpen"]
                self.game.player.interacting = False
                self.game.player.money += 500
                self.game.progress = 0
                self.status = False