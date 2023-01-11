# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Camera: #

class Camera(pygame.sprite.Sprite):
    def __init__(self, game, tile_size, assets_manager, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Game: 

        self.game = game

        # Assets Manager:

        self.assets_manager = assets_manager

        # World: 

        self.tile_size = tile_size

        # Camera Directions:

        self.direction = random.randint(0, 1)
        self.camera_directions = [x - (self.tile_size * 5.5), x - (self.tile_size * -1.2)]

        # Camera Settings:

        self.image = self.assets_manager.camera[f"Camera{self.direction}"]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.tile_size // 2, y + (self.tile_size - self.image.get_height()))

        # Camera Vision:

        self.camera_vision = pygame.Rect(self.camera_directions[self.direction], self.rect.y, self.game.screen_width // 6, self.game.screen_height // 9)

        # Camera Timer:

        self.camera_timer = pygame.time.get_ticks()
        self.camera_change_direction = 5000
        self.bar_time = (pygame.time.get_ticks() - self.camera_timer) / self.camera_change_direction

    def draw(self):
        self.game.display.blit(self.image, self.rect)
        pygame.draw.rect(self.game.display, (100, 144, 44), (self.rect.x, self.rect.bottom - self.rect.h // 5, (self.rect.w), self.game.screen_width // 256))
        pygame.draw.rect(self.game.display, (0, 255, 40), (self.rect.x, self.rect.bottom - self.rect.h // 5, (self.rect.w) * (self.bar_time), self.game.screen_width // 256))
        pygame.draw.rect(self.game.display, (0, 0, 0), (self.rect.x, self.rect.bottom - self.rect.h // 5,(self.rect.w), self.game.screen_width // 256), 2)

    def update(self):
        if(pygame.time.get_ticks() - self.camera_timer > self.camera_change_direction):
            if(self.direction == 1):
                self.direction = 0
            else:
                self.direction += 1

            self.image = self.assets_manager.camera[f"Camera{self.direction}"]
            self.camera_vision = pygame.Rect(self.camera_directions[self.direction], self.rect.y, self.game.screen_width // 6, self.game.screen_height // 9)
            self.camera_timer = pygame.time.get_ticks()

        if(self.camera_vision.colliderect(self.game.player)):
            self.game.player.moving = False
            self.game.sounds.play_sound('Alarm', 0.1)
            self.game.sounds.stop_sound('Footsteps')
            self.game.sounds.stop_music()
            self.game.state = False

        self.bar_time = (pygame.time.get_ticks() - self.camera_timer) / self.camera_change_direction