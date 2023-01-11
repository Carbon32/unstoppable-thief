# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon                           #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Particles: #

class Particles():
    def __init__(self, game):

        # Game:

        self.game = game

        # Particle Groups:

        self.particles = {
            'run' : [],
            'jump' : []
        }

    def circle_surface(self, radius, color):
        surface = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surface, color, (radius, radius), radius)
        surface.set_colorkey((0, 0, 0))
        return surface

    def add_game_particle(self, particle_type, x, y ):
        particle_type.lower()
        if(particle_type == "run"):
            self.particles['run'].append([[x + random.randint(-self.game.screen_width // 80, self.game.screen_width // 80), y], [random.randint(-4, 4), -0.5], random.randint(self.game.screen_width // 1024, self.game.screen_width // 512)])

        elif(particle_type == "jump"):
            self.particles['jump'].append([[x, y], [0, -2], random.randint(self.game.screen_width // 256, self.game.screen_width // 256)])

        else:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def draw_game_particles(self, particle_type, color):
        try:
            for particle in self.particles[particle_type]:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.05
                pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if(particle[2] <= 0):
                    self.particles[particle_type].remove(particle)
        except KeyError:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def draw_particles(self):
        self.draw_game_particles("run", (255, 255, 255))
        self.draw_game_particles("jump", (160, 82, 45))