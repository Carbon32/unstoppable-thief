# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Thief, platformer video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game Window: #

window = Window(990, 1000, "Unstoppable Thief:")
window.init()

# Game Variables: #

mainMenu = True

# Game Icon: #

setGameIcon('assets/Enemy/Arrest/0.png')

# Music: #
playMusic("sounds/music.mp3", 0.1)

# Sounds: #
coinSound = loadGameSound('sounds/coin.wav', 0.2)
deathSound = loadGameSound('sounds/death.wav', 0.2)
jumpSound = loadGameSound('sounds/jump.wav', 0.2)
arrestSound = loadGameSound('sounds/arrest.wav', 0.2)
assignGameSounds(coinSound, jumpSound, arrestSound, deathSound)

# Background: #

menuBackground = loadStaticImage('assets/Menu/menu.png')

# Buttons: #

restartImage = loadStaticImage('assets/Buttons/restart.png')
startImage = loadStaticImage('assets/Buttons/start.png')
exitImage = loadStaticImage('assets/Buttons/exit.png')

# Game Mechanics: #

# World:
worldData = assignWorldTiles()
world = World(worldData)

# Player:
player = Player(100, 100)

# Buttons:
restartButton = Button(window.screenWidth // 2 - 120, window.screenHeight // 2 + 50, restartImage)
startButton = Button(window.screenWidth // 2 - 120, window.screenHeight // 2 - 200, startImage)
exitButton = Button(window.screenWidth // 2 - 120, window.screenHeight // 2, exitImage)


# Game Loop: #

while(window.engineRunning):
	window.limitFPS(60)
	window.setBackground((100, 123, 255))
	if(mainMenu == True):
		window.setMenuBackground(menuBackground)
		if(startButton.draw(window.engineWindow)):
			mainMenu = False

		if(exitButton.draw(window.engineWindow)):
			window.engineRunning = False
	else:
		drawGameSprites(window.engineWindow, world)
		if(checkGameState() == -1):
			drawText(window.engineWindow, 'GAME OVER', (255, 50, 50), 70, window.screenWidth // 2 - 130, window.screenHeight // 2 - 100)
			if(restartButton.draw(window.engineWindow)):
				worldData = resetLevel(worldData)
				world = World(worldData)
		elif(checkGameState() == 1):
			worldData = loadNextLevel(worldData)
			world = World(worldData)
			
		else:
			updateGameMechanics()
	window.updateDisplay()