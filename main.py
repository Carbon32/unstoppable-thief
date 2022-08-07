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

# Assets Manager: #

assetsManager = AssetsManager(game)

# World: #

world = World(game)

# Menu: #

menu = Menu(game, world, assetsManager)

# Editor: #

editor = Editor(game, world, assetsManager, menu)

# Particles: #

particles = Particles(game)

# Loading Tiles: #

world.loadTiles()
editor.loadTiles()

# Generate World: 

world.setGameLevel(game.level)

# Fade In:

gameFade = Fade(game, 1, ((0, 0, 0)))

# Game Loop: #

while(game.engineRunning):

	game.setBackground((63, 56, 81))
	
	if(game.menuOn):

		menu.handleMenu()
		gameFade.reset()

	else:

		if(game.editorStatus):

			editor.generateEditorWorld()
			editor.drawWorld()
			editor.drawGrid()
			editor.drawUserInterface()
			editor.drawInformation()
			editor.handleButtons()
			if(gameFade.fade()):

				editor.handleEditor()
		else:

			game.drawGameSprites(world)
			particles.drawParticles()
			game.updateGameSprites(world, particles)

			if(gameFade.fade()):

				game.startGame()

	game.updateDisplay(60)
	print(game.fpsHandler.get_fps())