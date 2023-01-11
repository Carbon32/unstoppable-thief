# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Editor: #

class Editor():
    def __init__(self, game, world, assets_manager, menu):

        # Game:

        self.game = game

        # World:

        self.world = world
        self.world_generated = False

        # Assets Manager:

        self.assets_manager = assets_manager

        # Menu:

        self.menu = menu

        # Editor Settings:

        self.unsaved = False
        self.this_tile = 0

        # Tile Selection:

        self.editor_tile_size = self.game.screen_width // 42
        self.tile_buttons = []
        self.tile_column = 0
        self.tile_row = 0
        self.this_tile = 0

        # User Interface:

        self.interface_ready = False
        self.button_count = 0
        self.side_margin = pygame.Rect(self.game.screen_width - self.game.screen_width // 4, 0, self.game.screen_width // 4, self.game.screen_height)
        self.lower_margin = pygame.Rect(0, self.game.screen_height - self.game.screen_height // 4, self.game.screen_width, self.game.screen_height // 4)
        
        # Buttons:

        self.save_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 18), self.game.screen_height - (self.game.screen_height // 12), self.assets_manager.buttons["Save"])
        self.clear_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 3), self.game.screen_height - (self.game.screen_height // 12), self.assets_manager.buttons["Clear"])
        self.back_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 5), self.game.screen_height - (self.game.screen_height // 12), self.assets_manager.buttons["Back"])

        # Timer:

        self.change_timer = pygame.time.get_ticks()

        # Editor Tiles List:

        self.editor_tiles = []

    def load_tiles(self):
        for tile in self.world.available_tiles:
            image = pygame.transform.scale(tile, (self.editor_tile_size, self.editor_tile_size))
            self.editor_tiles.append(image)

    def load_new_level(self):
        with open(f'levels/level{self.game.level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world.world_data[x][y] = int(tile)

    def generate_editor_world(self):
        if(not self.world_generated):
            for row in range(self.world.level_columns):
                r = [-1] * self.world.level_columns
                self.world.world_data.append(r)
            self.world_generated = True

    def draw_grid(self):
        for c in range(self.world.level_columns + 1):
            pygame.draw.line(self.game.display, ((255, 255, 255)), (c * self.editor_tile_size, 0), (c * self.editor_tile_size, self.game.screen_height))

        for c in range(self.world.level_rows + 1):
            pygame.draw.line(self.game.display, ((255, 255, 255)), (0, c * self.editor_tile_size), (self.game.screen_width, c * self.editor_tile_size))

    def draw_world(self):
        for y, row in enumerate(self.world.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.game.display.blit(self.editor_tiles[tile], (x * self.editor_tile_size, y * self.editor_tile_size))

    def draw_user_interface(self):
        pygame.draw.rect(self.game.display, ((140, 146, 172)), self.side_margin)
        pygame.draw.rect(self.game.display, ((140, 146, 172)), self.lower_margin)
        if(self.interface_ready == False):
            for i in range(len(self.world.available_tiles)):
                tile_button = Button(self.game.display, self.game.screen_width - ((self.game.screen_width // 20) * self.tile_column) - (self.game.screen_width // 16), ((self.game.screen_width // 25) * self.tile_row) + (self.game.screen_height // 20), self.editor_tiles[i])
                self.tile_buttons.append(tile_button)
                self.tile_column += 0.8
                if self.tile_column == 4:
                    self.tile_row += 0.8
                    self.tile_column = 0

            self.interface_ready = True

        self.button_count = 0
        for self.button_count, button in enumerate(self.tile_buttons):
            if button.render():
                self.this_tile = self.button_count

        for tile in range (len(self.tile_buttons)):
            pygame.draw.rect(self.game.display, ((0, 0, 0)), self.tile_buttons[tile].rect, self.game.screen_width // 512)

        pygame.draw.rect(self.game.display, ((255, 0, 0)), self.tile_buttons[self.this_tile].rect, self.game.screen_width // 256)

    def draw_information(self):
        if(self.unsaved):
            self.game.draw_text(self.game.display, "Unsaved", self.game.screen_width // 64, (255, 20, 10), self.game.screen_width // 20, self.game.screen_height - (self.game.screen_height // 18))

        self.game.draw_text(self.game.display, f"Level: {self.game.level}", self.game.screen_width // 64, (0, 0, 0), self.game.screen_width // 20, self.game.screen_height - (self.game.screen_height // 12))

    def handle_buttons(self):
        i = 0
        if(self.save_button.render() and self.unsaved):
            with open(f'levels/level{self.game.level}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',')
                for row in self.world.world_data:
                    if(i >= self.world.level_rows):
                        break
                    writer.writerow(row)
                    i += 1

            self.unsaved = False

        if(self.clear_button.render()):
            self.world.world_data = []
            for row in range(self.world.level_rows):
                r = [-1] * self.world.level_columns
                self.world.world_data.append(r)

            for tile in range(0, self.world.level_columns):
                self.world.world_data[self.world.level_rows - 1][tile] = 0

            self.unsaved = True

        if(self.back_button.render()):
            self.menu.main_menu = True
            self.game.menu_on = True
            self.game.editor_status = False
            self.game.level_selector = True

    def handle_editor(self):
        position = pygame.mouse.get_pos()
        x = (position[0]) // self.editor_tile_size
        y = position[1] // self.editor_tile_size
        if(pygame.key.get_pressed()[pygame.K_z]):
            if(pygame.time.get_ticks() - self.change_timer > 200 and self.game.level < 3):
                self.game.level += 1
                self.unsaved = False
                self.load_new_level()
                self.change_timer = pygame.time.get_ticks()

        if(pygame.key.get_pressed()[pygame.K_s]):
            if(pygame.time.get_ticks() - self.change_timer > 200 and self.game.level != 1):
                self.game.level -= 1
                self.unsaved = False
                self.load_new_level()
                self.change_timer = pygame.time.get_ticks()

        if(position[0] < self.game.screen_width and position[1] < self.game.screen_height):
            if(not self.side_margin.collidepoint(position) and not self.lower_margin.collidepoint(position)):
                if (pygame.mouse.get_pressed()[0] == 1):
                    if (self.world.world_data[y][x] != self.this_tile):
                        self.world.world_data[y][x] = self.this_tile
                        self.unsaved = True

                if (pygame.mouse.get_pressed()[2] == 1):
                    if(not self.world.world_data[y][x] == -1):
                        self.world.world_data[y][x] = -1
                        self.unsaved = True