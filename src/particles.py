# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon               		      #
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

		self.burn_particles = []
		self.run_particles = []
		self.jump_particles = []

	def circle_surface(self, radius, color):
		surface = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surface, color, (radius, radius), radius)
		surface.set_colorkey((0, 0, 0))
		return surface

	def add_game_particle(self, particle_type, x, y ):
		particle_type.lower()
		if(particle_type == "lava"):
			self.burn_particles.append([[x, y], [0, -3], random.randint(12, 18)])

		elif(particle_type == "run"):
			self.run_particles.append([[x + random.randint(-self.game.screen_width // 80, self.game.screen_width // 80), y], [random.randint(-4, 4), -0.5], random.randint(self.game.screen_width // 1024, self.game.screen_width // 512)])

		elif(particle_type == "enemy"):
			self.run_particles.append([[x, y], [random.randint(-2, 2), -1], random.randint(1, 3)])

		elif(particle_type == "jump"):
			self.jump_particles.append([[x, y], [0, -2], random.randint(self.game.screen_width // 256, self.game.screen_width // 256)])

		else:
			print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

	def draw_game_particles(self, particle_type, color):
		if(particle_type == "lava"):
			for particle in self.burn_particles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.game.display.blit(circle_surface(radius, color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				if(particle[2] <= 0):
					self.burn_particles.remove(particle)

		elif(particle_type == "run"):
			for particle in self.run_particles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.05
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.run_particles.remove(particle)

		elif(particle_type == "enemy"):
			for particle in self.run_particles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.run_particles.remove(particle)

		elif(particle_type == "jump"):
			for particle in self.jump_particles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.jump_particles.remove(particle)

		else:
			print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

	def draw_particles(self):
		self.draw_game_particles("run", (255, 255, 255))
		self.draw_game_particles("jump", (160, 82, 45))