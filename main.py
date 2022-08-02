# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Thief, platformer video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game: #

game = Game()

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolutionStatus):

    resolution.updateBackground()

    if(resolution.resolutionA.render()):

        resolution.setResolution(1280, 720)
        break

    if(resolution.resolutionB.render()):

        resolution.setResolution(1920, 1080)

        break

    resolution.updateWindow()

# Game Window: #

game.startWindow()

# Game Icon: #

game.setGameIcon('assets/Player/Move/0.png')

# Particles: #

particles = Particles(game)

# World: #

world = World(game)

# Tiles: #

world.loadTiles()
world.setGameLevel(1)

# Game Loop: #

while(game.engineRunning):
	game.setBackground((0, 100, 255))

	game.updateGameSprites(world, particles)
	particles.drawParticles()
	game.drawGameSprites(world)
	game.updateDisplay(60)
	print(game.fpsHandler.get_fps())
