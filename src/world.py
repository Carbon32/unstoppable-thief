# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.player import *
from src.object import *
from src.camera import *
from src.safe import *
from src.money import *
from src.key import *

# World: #

class World():
    def __init__(self, game, assets_manager):

        # Game:

        self.game = game

        # Assets Manager:

        self.assets_manager =  assets_manager

        # Level Settings:

        self.level_rows = 18
        self.level_columns = 32

        # Tiles:

        self.tile_size = self.game.screen_width // 32
        self.available_tiles = []

        # World Settings:

        self.world_data = []

        # World Objects:

        self.obstacle_list = []

    def load_tiles(self):
        for c in range(len(os.listdir('assets/Tiles'))):
            image = self.game.load_game_image(f'assets/Tiles/{c}.png', self.tile_size, self.tile_size)
            self.available_tiles.append(image)

    def set_game_level(self, level):

        # Generate An Empty World:

        for r in range(self.level_rows):
            row = [-1] * self.level_columns
            self.world_data.append(row)

        # Load a new level:

        with open(f'levels/level{level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        # Remove all sprites:

        self.game.remove_all_sprites()

        # Reset Player Position:

        self.game.player = Player(self.game, self.game.screen_width // 10, self.game.screen_height - (self.game.screen_height // 8), self.game.screen_width // 300)

        # Update Game Level:

        self.game.level = level

        # Generate World:

        self.obstacle_list = []
        self.generate_world()

    def generate_world(self):
        self.level_length = len(self.world_data[0])
        for y, row in enumerate(self.world_data):
            for x, t in enumerate(row):
                if(t >= 0):
                    tile = self.available_tiles[t]
                    tile_rect = tile.get_rect()
                    tile_rect.x = x * self.tile_size
                    tile_rect.y = (y * self.tile_size)
                    tile_data = (tile, tile_rect)
                    if(t >= 0 and t <= 10):
                        self.obstacle_list.append(tile_data)

                    if(t >= 11 and t <= 75):
                        object = Object(self.game, self.tile_size, tile, x * self.tile_size, (y * self.tile_size))
                        self.game.objects_group.add(object)

                    if(t == 76):
                        exit = Object(self.game, self.tile_size, tile, x * self.tile_size, (y * self.tile_size))
                        self.game.exit_group.add(exit)

                    if(t == 77):
                        safe = Safe(self.game, self.tile_size, self.assets_manager, x * self.tile_size, (y * self.tile_size))
                        self.game.safes_group.add(safe)

                    if(t == 78):
                        money = Money(self.game, self.tile_size, self.assets_manager, x * self.tile_size, (y * self.tile_size))
                        self.game.money_group.add(money)

                    if(t == 79):
                        key = Key(self.game, self.tile_size, self.assets_manager, x * self.tile_size, (y * self.tile_size))
                        self.game.keys_group.add(key)

                    if(t == 80):
                        camera = Camera(self.game, self.tile_size, self.assets_manager, x * self.tile_size, (y * self.tile_size))
                        self.game.camera_group.add(camera)

    def render(self):
        for tile in self.obstacle_list:
            self.game.display.blit(tile[0], tile[1])