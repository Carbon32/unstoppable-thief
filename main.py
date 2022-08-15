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

# Sounds: #

sounds = Sounds()

# Game Window: #

game.startWindow(sounds)

# Game Icon: #

game.setGameIcon('assets/Player/Move/0.png')

# Assets Manager: #

assetsManager = AssetsManager(game)

# User Interface: #

ui = UserInterface(game, assetsManager)

# World: #

world = World(game, assetsManager)

# Menu: #

menu = Menu(game, world, assetsManager)

# Editor: #

editor = Editor(game, world, assetsManager, menu)

# Particles: #

particles = Particles(game)

# Loading Tiles: #

world.loadTiles()
editor.loadTiles()

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

			menu.checkForArrest()
			game.drawGameSprites(world, ui)
			particles.drawParticles()
			game.updateGameSprites(world, particles)

			if(gameFade.fade()):

				game.startGame()

	game.updateDisplay(60)