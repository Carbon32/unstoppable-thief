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

# Game Window: #

game.startWindow()

# Game Icon: #

game.setGameIcon('assets/Player/Move/0.png')

# World: #

world = World(game)

# Tiles: #

world.loadTiles()
world.setGameLevel(1)

# Game Loop: #

while(game.engineRunning):
	game.setBackground((0, 100, 255))

	game.updateGameSprites(world)
	game.drawGameSprites(world)
	game.updateDisplay(60)
	print(game.fpsHandler.get_fps())
