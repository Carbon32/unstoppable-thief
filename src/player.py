# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.particles import *

# Player: #

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x : int, y : int, speed : int):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Player Settings: 

        self.x = x
        self.y = y
        self.default_speed = speed
        self.speed = speed
        self.sprint = 500
        self.max_sprint = self.sprint
        self.interacting = False

        # Player Items:

        self.money = 0
        self.key = False

        # Player Movement Variables:

        self.direction = 1
        self.move_right = False
        self.move_left = False
        self.moving = False
        self.velocity_y = 0
        self.in_air = False
        self.jump = False
        self.sprinting = False
        self.footsteps_playing = False

        # Player Animation Variables:

        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0

        # Player Sound:

        self.sound_length = 0
        self.sound_time = pygame.time.get_ticks()

        # Collision Patches:

        self.x_collision = self.game.screen_width // 44
        self.y_collision = self.game.screen_width // 31

        # Player Timers:

        self.time = pygame.time.get_ticks()

        # Loading Sprites:

        animation_types = ['Idle', 'Move', 'Jump', 'Crack']
        for animation in animation_types:
            temp_list = []
            frames_number = len(os.listdir(f'assets/Player/{animation}'))
            for c in range(frames_number): # Loading all animations
                game_image = pygame.image.load(f'assets/Player/{animation}/{c}.png').convert_alpha()
                game_image = pygame.transform.scale(game_image, (self.game.screen_width // 16, self.game.screen_height // 8))
                temp_list.append(game_image)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = pygame.Rect(x, y, self.image.get_width() - self.game.screen_width // 24, self.image.get_height() // 1.8)
        self.rect.center = (x, y)

    def update(self, world, particles):
        if(self.game.game_ready):
            if(not self.interacting):
                if(pygame.key.get_pressed()[pygame.K_LSHIFT] and (self.move_right or self.move_left)):
                    if(self.sprint > 0):
                        self.sprinting = True
                        self.sprint -= 2
                    else:
                        self.sprint = 0
                        self.sprinting = False

                if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.game.game_ready):
                    self.game.menu_on = True
                    self.game.sounds.stop_music()

                if(pygame.key.get_pressed()[pygame.K_d]):
                    self.move_right = True
                    self.moving = True
                    self.update_action(1)
                    if(not self.in_air):
                        particles.add_game_particle('run', self.rect.centerx, self.rect.bottom)

                if(pygame.key.get_pressed()[pygame.K_q]):
                    self.move_left = True
                    self.moving = True
                    self.update_action(1)
                    if(not self.in_air):
                        particles.add_game_particle('run', self.rect.centerx, self.rect.bottom)

                if(pygame.key.get_pressed()[pygame.K_SPACE] and self.in_air == False):
                    self.jump = True
                    particles.add_game_particle('jump', self.rect.centerx, self.rect.bottom)

        if(not pygame.key.get_pressed()[pygame.K_d]):
                self.move_right = False

        if(not pygame.key.get_pressed()[pygame.K_q]):
                self.move_left = False

        if(not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_d]):
            self.moving = False
            self.update_action(0)

        if(not pygame.key.get_pressed()[pygame.K_LSHIFT]):
            self.sprinting = False

            if(not self.sprint == self.max_sprint):
                self.sprint += 1

        delta_x = 0
        delta_y = 0

        if(self.interacting):
            self.game.sounds.stop_sound('Footsteps')
            self.move_left = False
            self.move_right = False
            self.update_action(3)

        if(self.move_left):
            delta_x = -self.speed
            self.flip = True
            self.direction = -1

        if(self.move_right):
            delta_x = self.speed
            self.flip = False
            self.direction = 1

        if(self.jump == True and self.in_air == False):
            if(self.game.screen_width == 1920):
                self.velocity_y = -(world.tile_size // 3.6)
            else:
                self.velocity_y = -(world.tile_size // 3.4)

            self.jump = False
            self.in_air = True

        if(self.sprinting):
            self.speed = self.default_speed * 1.5

        if(not self.sprinting):
            self.speed = self.default_speed

        if(self.in_air):
            self.footsteps_playing = False
            self.game.sounds.stop_sound('Footsteps')
            self.update_action(2)

        if(self.sound_length == round(pygame.mixer.Sound.get_length(self.game.sounds.sounds['Footsteps']))):
            self.game.sounds.stop_sound('Footsteps')
            self.game.sounds.play_sound('Footsteps', 0.1)
            self.sound_length = 0

        if(pygame.time.get_ticks() - self.sound_time > 1000):
            self.sound_length += 1
            self.sound_time = pygame.time.get_ticks()

        if(self.moving):
            if(not self.footsteps_playing):
                self.game.sounds.stop_sound('Footsteps')
                self.game.sounds.play_sound('Footsteps', 0.1)
                self.footsteps_playing = True

        if(not self.moving):
            self.footsteps_playing = False
            self.game.sounds.stop_sound('Footsteps')

        self.velocity_y += self.game.engine_gravity
        delta_y += self.velocity_y
        for tile in world.obstacle_list:
            if(tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.rect.w, self.rect.h)):
                delta_x = 0

            if(tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.rect.w, self.rect.h)):
                if(self.velocity_y < 0):
                    self.velocity_y = 0
                    delta_y = tile[1].bottom - self.rect.top

                elif(self.velocity_y >= 0):
                    self.velocity_y = 0
                    if(self.in_air):
                        self.in_air = False

                    delta_y = tile[1].top - self.rect.bottom

        if(self.rect.left + delta_x < 0 or self.rect.right + delta_x > self.game.screen_width):
            delta_x = 0

        if(pygame.sprite.spritecollide(self, self.game.exit_group, False)):
            if(self.key):
                if(self.game.level == 3):
                    self.game.level = 1
                else:
                    self.game.level += 1

                self.game.sounds.play_sound('Door', 0.1)
                self.money = 0
                self.key = False
                self.game.seconds = [0, 0]
                self.game.minutes = [0, 0]
                world.set_game_level(self.game.level)
                self.rect.x, self.rect.y = self.game.screen_width // 10, self.game.screen_height - (self.game.screen_height // 8)

        self.rect.x += delta_x
        self.rect.y += delta_y
        self.update_animation()

    def update_animation(self):
        if(self.move_left or self.move_right):
            if(self.sprinting):
                animation_time = 60
            else:
                animation_time = 80
        else:
            animation_time = 140

        self.image = self.animation_list[self.action][self.index]
        if(pygame.time.get_ticks() - self.time > animation_time):
            self.time = pygame.time.get_ticks()
            self.index += 1

        if(self.index >= len(self.animation_list[self.action])):
            if(self.action == 2):
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index = 0

    def update_action(self, new_action):
        if(new_action != self.action):
            self.action = new_action
            self.index = 0
            self.time = pygame.time.get_ticks()


    def render(self):
        self.game.display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.x_collision, self.rect.y - self.y_collision))

        # Sprint Bar:

        pygame.draw.rect(self.game.display, (30,144,255), (self.game.screen_width // 3, (self.game.screen_height // 4 - self.game.screen_height // 4.3), (self.rect.w * 3), self.game.screen_width // 80))
        pygame.draw.rect(self.game.display, (173,216,230), (self.game.screen_width // 3, (self.game.screen_height // 4 - self.game.screen_height // 4.3), (self.rect.w * 3) * (self.sprint / self.max_sprint), self.game.screen_width // 80))
        pygame.draw.rect(self.game.display, (255, 255, 255), (self.game.screen_width // 3, (self.game.screen_height // 4 - self.game.screen_height // 4.3),(self.rect.w * 3), self.game.screen_width // 80), 2)
