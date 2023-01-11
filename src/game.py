# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.player import *

# Game: #

class Game():
    def __init__(self):

        # Display:

        self.screen_width = 1920
        self.screen_height = 1080
        self.engine_running = False
        self.fps_handler = pygame.time.Clock()

        # Game Status:

        self.game_ready = False

        # Level State:

        self.state = True

        # Editor Status:

        self.editor_status = False

        # Level Selector:

        self.level_selector = True

        # Music:

        self.music_started = False

        # Menu Status:

        self.menu_on = True

        # Level:

        self.level = 1

        # Sprite Groups:

        self.enemy_group = pygame.sprite.Group()
        self.money_group = pygame.sprite.Group()
        self.safes_group = pygame.sprite.Group()
        self.keys_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.objects_group = pygame.sprite.Group()
        self.camera_group = pygame.sprite.Group()

        # Timer:

        self.change_time = False
        self.time_update = pygame.time.get_ticks()
        self.seconds = [0, 0]
        self.minutes = [0, 0]

        # Cracking Progress:

        self.progress = 0

    def start_game(self):
        self.game_ready = True
        self.change_time = True
        if(not self.music_started):
            self.sounds.play_music('sounds/background/background.ogg', 0.06)
            self.music_started = True

    def set_game_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def start_window(self, sounds):
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption("Unstoppable Thief")
        self.engine_gravity = (self.screen_width // 300) * 0.1
        self.player = Player(self, 0, 0, 0)
        self.sounds = sounds
        self.engine_running = True
        self.fonts = {
            'huge' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 14),
            'large' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 20),
            'small' : pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 48)
        }

    def update_display(self, fps):
        self.fps_handler.tick(fps)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.engine_running = False

        pygame.display.update()

    def load_game_sound(self, path):
        sound = pygame.mixer.Sound(path)
        return sound

    def load_game_image(self, path, width, height):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def draw_text(self, text, size, color, x, y):
        image = pygame.font.SysFont('System', size).render(text, True, color)
        self.display.blit(image, (x, y))

    def draw_custom_text(self, font, text, color, x, y):
        image = font.render(text, True, color)
        self.display.blit(image, (x, y))

    def update_time(self):
        if(self.change_time):
            if(pygame.time.get_ticks() - self.time_update > 1):
                self.seconds[1] += 1
                if(self.seconds[1] == 9 and self.seconds[0] != 5):
                    self.seconds[0] += 1
                    self.seconds[1] = 0

                if(self.seconds[0] == 5 and self.seconds[1] == 9):
                    self.minutes[1] += 1
                    self.seconds[0] = 0
                    self.seconds[1] = 0

                if(self.minutes[1] == 9):
                    self.minutes[0] += 1
                    self.minutes[1] = 0

            self.time_update = pygame.time.get_ticks()

    def set_background(self, rgb : tuple):
        self.display.fill(rgb)

    def remove_all_sprites(self):
        self.enemy_group.empty()
        self.money_group.empty()
        self.safes_group.empty()
        self.keys_group.empty()
        self.exit_group.empty()
        self.objects_group.empty()
        self.camera_group.empty()

    def update_game_sprites(self, world, particles):
        if(self.state):
            self.player.update(world, particles)
            for money in self.money_group:
                money.update()

            for safe in self.safes_group:
                safe.update()

            for key in self.keys_group:
                key.update()

            for camera in self.camera_group:
                camera.update()

            self.update_time()

    def draw_game_sprites(self, world, ui):
            for object in self.objects_group:
                object.draw()

            for money in self.money_group:
                money.draw()

            for safe in self.safes_group:
                safe.draw()

            for key in self.keys_group:
                key.draw()

            for camera in self.camera_group:
                camera.draw()

            for exit in self.exit_group:
                exit.draw()

            world.render()
            ui.draw_stats()
            self.player.render()
