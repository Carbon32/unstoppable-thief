# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon               		      #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
	import pygame 
	import random
	import csv
	import os
	from pygame import mixer

except ImportError:
	raise ImportError("The Unstoppable Engine couldn't import all of the necessary packages.")
  
# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()

# Engine Functions: #

def loadGameImage(path : str, width : int, height : int):
	image = pygame.image.load(path).convert_alpha()
	image = pygame.transform.scale(image, (width, height))
	return image

def drawText(display : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
	image = pygame.font.SysFont('System', size).render(text, True, color)
	display.blit(image, (x, y))

# Game: #

class Game():
	def __init__(self):

		# Display:

		self.screenWidth = 1920
		self.screenHeight = 1080
		self.engineRunning = False
		self.fpsHandler = pygame.time.Clock()

		# Game Status:

		self.gameReady = False

		# Editor Status:

		self.editorStatus = False

		# Menu Status:

		self.menuOn = True

		# Level:

		self.level = 1

		# Sprite Groups:

		self.enemyGroup = pygame.sprite.Group()
		self.lavaGroup = pygame.sprite.Group()
		self.exitGroup = pygame.sprite.Group()
		self.coinsGroup = pygame.sprite.Group()
		self.platformGroup = pygame.sprite.Group()
		self.objectsGroup = pygame.sprite.Group()

	def startGame(self):

		self.gameReady = True

	def setGameIcon(self, path : str):
		icon = pygame.image.load(path)
		pygame.display.set_icon(icon)

	def startWindow(self):
		self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		pygame.display.set_caption("Unstoppable Thief")
		self.engineGravity = (self.screenWidth // 300) * 0.1
		self.player = Player(self, self.screenWidth // 10, self.screenHeight - (self.screenHeight // 8), self.screenWidth // 300)
		self.engineRunning = True

	def updateDisplay(self, fps : int):
		self.fpsHandler.tick(fps)

		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False

		if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
			self.engineRunning = False

		pygame.display.update()

	def setBackground(self, rgb : tuple):
		self.display.fill(rgb)

	def removeAllSprites(self):
		self.enemyGroup.empty()
		self.lavaGroup.empty()
		self.exitGroup.empty()
		self.coinsGroup.empty()
		self.platformGroup.empty()

	def updateGameSprites(self, world, particles):

		self.player.update(world, particles)

	def drawGameSprites(self, world):

			for object in self.objectsGroup:

				object.draw()

			world.render()
			self.player.render()

# Player: #

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, speed : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Player Settings: 

		self.x = x
		self.y = y
		self.defaultSpeed = speed
		self.speed = speed
		self.health = 100
		self.maxHealth = self.health
		self.sprint = 500
		self.maxSprint = self.sprint

		# Player Movement Variables:

		self.direction = 1
		self.moveRight = False
		self.moveLeft = False
		self.velocityY = 0
		self.inAir = False
		self.jump = False
		self.sprinting = False

		# Player Animation Variables:

		self.flip = False
		self.animationList = []
		self.index = 0
		self.action = 0

		# Collision Patches:

		self.xcollision = self.game.screenWidth // 44
		self.ycollision = self.game.screenWidth // 31

		# Player Timers:

		self.time = pygame.time.get_ticks()

		# Loading Sprites:

		animationTypes = ['Idle', 'Move', 'Jump']
		for animation in animationTypes:

			tempList = []
			framesNumber = len(os.listdir(f'assets/Player/{animation}'))

			for c in range(framesNumber): # Loading all animations

				gameImage = pygame.image.load(f'assets/Player/{animation}/{c}.png').convert_alpha()
				gameImage = pygame.transform.scale(gameImage, (self.game.screenWidth // 16, self.game.screenHeight // 8))
				tempList.append(gameImage)

			self.animationList.append(tempList)

		self.image = self.animationList[self.action][self.index]
		self.rect = pygame.Rect(x, y, self.image.get_width() - self.game.screenWidth // 24, self.image.get_height() // 1.8)
		self.rect.center = (x, y)

	def update(self, world, particles):

		if(self.game.gameReady):

			if(pygame.key.get_pressed()[pygame.K_LSHIFT] and (self.moveRight or self.moveLeft)):

				if(self.sprint > 0):

					self.sprinting = True
					self.sprint -= 2

				else:

					self.sprint = 0
					self.sprinting = False

			if(pygame.key.get_pressed()[pygame.K_d]):

				self.moveRight = True
				self.updateAction(1)
				if(not self.inAir):
					
					particles.addGameParticle('run', self.rect.centerx, self.rect.bottom)

			if(pygame.key.get_pressed()[pygame.K_q]):

				self.moveLeft = True
				self.updateAction(1)
				if(not self.inAir):
					
					particles.addGameParticle('run', self.rect.centerx, self.rect.bottom)

			if(pygame.key.get_pressed()[pygame.K_SPACE] and self.inAir == False):

				self.jump = True
				particles.addGameParticle('jump', self.rect.centerx, self.rect.bottom)

		if(not pygame.key.get_pressed()[pygame.K_d]):

				self.moveRight = False

		if(not pygame.key.get_pressed()[pygame.K_q]):

				self.moveLeft = False

		if(not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_d]):

			self.updateAction(0)

		if(not pygame.key.get_pressed()[pygame.K_LSHIFT]):

			self.sprinting = False

			if(not self.sprint == self.maxSprint):

				self.sprint += 1

		deltaX = 0
		deltaY = 0

		if(self.moveLeft):

			deltaX = -self.speed
			self.flip = True
			self.direction = -1

		if(self.moveRight):

			deltaX = self.speed
			self.flip = False
			self.direction = 1

		if(self.jump == True and self.inAir == False):
			if(self.game.screenWidth == 1920):

				self.velocityY = -(world.tileSize // 3.6)

			else:

				self.velocityY = -(world.tileSize // 3.4)

			self.jump = False
			self.inAir = True

		if(self.sprinting):

			self.speed = self.defaultSpeed * 1.5

		if(not self.sprinting):

			self.speed = self.defaultSpeed

		if(self.inAir):

			self.updateAction(2)

		self.velocityY += self.game.engineGravity

		deltaY += self.velocityY

		for tile in world.obstacleList:

			if(tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.rect.w, self.rect.h)):

				deltaX = 0

			if(tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.rect.w, self.rect.h)):

				if(self.velocityY < 0):

					self.velocityY = 0
					deltaY = tile[1].bottom - self.rect.top

				elif(self.velocityY >= 0):

					self.velocityY = 0

					if(self.inAir):
						
						self.inAir = False

					deltaY = tile[1].top - self.rect.bottom

		if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > self.game.screenWidth):
				
			deltaX = 0

		self.rect.x += deltaX
		self.rect.y += deltaY
		self.updateAnimation()

	def updateAnimation(self):

		if(self.moveLeft or self.moveRight):

			if(self.sprinting):

				animTime = 60

			else:

				animTime = 80

		else:

			animTime = 140

		self.image = self.animationList[self.action][self.index]

		if(pygame.time.get_ticks() - self.time > animTime):

			self.time = pygame.time.get_ticks()
			self.index += 1

		if(self.index >= len(self.animationList[self.action])):

			if(self.action == 2):

				self.index = len(self.animationList[self.action]) - 1

			else:

				self.index = 0

	def updateAction(self, newAction : int):
		if(newAction != self.action):

			self.action = newAction
			self.index = 0
			self.time = pygame.time.get_ticks()


	def render(self):
		self.game.display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.xcollision, self.rect.y - self.ycollision))

		# Health Bar:

		pygame.draw.rect(self.game.display, (250, 0, 0), (self.game.screenWidth // 7, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3), (self.rect.w * 3), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (0, 250, 0), (self.game.screenWidth // 7, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3), (self.rect.w * 3) * (self.health / self.maxHealth), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (255, 255, 255), (self.game.screenWidth // 7, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3),(self.rect.w * 3), self.game.screenWidth // 80), 2)

		# Sprint Bar:

		pygame.draw.rect(self.game.display, (30,144,255), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3), (self.rect.w * 3), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (173,216,230), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3), (self.rect.w * 3) * (self.sprint / self.maxSprint), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (255, 255, 255), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 4.3),(self.rect.w * 3), self.game.screenWidth // 80), 2)

# World: #

class World():
	def __init__(self, game):

		# Game:

		self.game = game

		# Level Settings:

		self.levelRows = 18
		self.levelColumns = 32

		# Tiles:

		self.tileSize = self.game.screenWidth // 32
		self.availableTiles = []

		# World Settings:

		self.worldData = []

		# World Objects:

		self.obstacleList = []

	def loadTiles(self):
		for c in range(len(os.listdir('assets/Tiles'))):

			image = loadGameImage(f'assets/Tiles/{c}.png', self.tileSize, self.tileSize)
			self.availableTiles.append(image)

	def setGameLevel(self, level : int):

		# Generate An Empty World:

		for r in range(self.levelRows):

			row = [-1] * self.levelColumns
			self.worldData.append(row)

		# Load a new level:

		with open(f'levels/level{self.game.level}.csv', newline='') as csvfile:

			reader = csv.reader(csvfile, delimiter=',')

			for x, row in enumerate(reader):

				for y, tile in enumerate(row):

					self.worldData[x][y] = int(tile)

		# Remove all sprites:

		self.game.removeAllSprites()

		# Update Game Level:

		self.game.level = level

		# Generate World:

		self.obstacleList = []
		self.generateWorld()

	def generateWorld(self):
		self.levelLength = len(self.worldData[0])

		for y, row in enumerate(self.worldData):

			for x, t in enumerate(row):

				if(t >= 0):

					tile = self.availableTiles[t]
					tileRect = tile.get_rect()
					tileRect.x = x * self.tileSize
					tileRect.y = (y * self.tileSize)
					tileData = (tile, tileRect)
					
					if(t >= 0 and t <= 10):

						self.obstacleList.append(tileData)

					if(t >= 11 and t <= 80):

						object = Object(self.game, self.tileSize, tile, x * self.tileSize, (y * self.tileSize))
						self.game.objectsGroup.add(object)

	def render(self):
		for tile in self.obstacleList:

			self.game.display.blit(tile[0], tile[1])

# Object: #

class Object(pygame.sprite.Sprite):
	def __init__(self, game, tileSize, image : pygame.Surface, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Game: 

		self.game = game

		# World: 

		self.tileSize = tileSize

		# Object Settings: 

		self.image = image
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.tileSize // 2, y + (self.tileSize - self.image.get_height()))
		self.rect.h = 1

	def draw(self):
		self.game.display.blit(self.image, self.rect)

# Menu:

class Menu():
	def __init__(self, game, world, assetsManager):

		# Game:

		self.game = game

		# World:

		self.world = world

		# Assets Manager:

		self.assetsManager = assetsManager

		#  Menu Settings: 

		self.mainMenu = True

		# Buttons:

		self.playButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 2 - (self.game.screenHeight // 3), self.assetsManager.buttons["Play"])
		self.editorButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 2 - (self.game.screenHeight // 6), self.assetsManager.buttons["Editor"])
		self.exitButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 6 + (self.game.screenHeight // 3), self.assetsManager.buttons["Exit"])

	def handleMenu(self):

		if(self.game.menuOn):

			self.game.setBackground((185, 189, 193))

			if(self.mainMenu):

				if(self.playButton.render()):

					self.mainMenu = False
					self.game.menuOn = False

				if(self.editorButton.render()):

					self.world.setGameLevel(self.game.level)
					self.game.editorStatus = True
					self.game.menuOn = False
					self.mainMenu = False

				if(self.exitButton.render()):

					self.game.engineRunning = False

# Assets Manager: 

class AssetsManager():
	def __init__(self, game):

		# Game:

		self.game = game

		# Buttons:

		self.buttons = {
			"Play" : loadGameImage('assets/Buttons/Play.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Editor" : loadGameImage('assets/Buttons/Editor.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Exit" : loadGameImage('assets/Buttons/Exit.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Again" : loadGameImage('assets/Buttons/Again.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Select" : loadGameImage('assets/Buttons/select.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Save" : loadGameImage('assets/Buttons/Save.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"Clear" : loadGameImage('assets/Buttons/Clear.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"Back" : loadGameImage('assets/Buttons/Back.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"MusicOn" : loadGameImage('assets/Buttons/musicOn.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"MusicOff" : loadGameImage('assets/Buttons/musicOff.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"SoundOn" : loadGameImage('assets/Buttons/soundOn.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"SoundOff" : loadGameImage('assets/Buttons/soundOff.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"Lvl1" : loadGameImage('assets/Buttons/Lvl_1.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl2" : loadGameImage('assets/Buttons/Lvl_2.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl3" : loadGameImage('assets/Buttons/Lvl_3.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl4" : loadGameImage('assets/Buttons/Lvl_4.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl5" : loadGameImage('assets/Buttons/Lvl_5.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl6" : loadGameImage('assets/Buttons/Lvl_6.png', self.game.screenWidth // 8, self.game.screenWidth // 16)
		}

# Resolution: #

class Resolution():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.resolutionWindow = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Unstoppable Thief: ")
		pygame.display.set_icon(loadGameImage('assets/icon.png', 32, 32))
		self.resolutionStatus = True

		# Background:

		self.background = loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.resolutionA = Button(self.resolutionWindow, 80, 200, loadGameImage('assets/Resolution/B.png', 150, 100)) # 1280 x 720
		self.resolutionB = Button(self.resolutionWindow, 80, 50, loadGameImage('assets/Resolution/A.png', 150, 100)) # 1920 x 1080

	def updateBackground(self):
		self.resolutionWindow.fill((255, 255, 255))
		self.resolutionWindow.blit(self.background, (0, 0))

	def setResolution(self, screenWidth : int, screenHeight : int):
		self.game.screenWidth = screenWidth
		self.game.screenHeight = screenHeight
		self.resolutionStatus = False


	def updateWindow(self):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				exit()

		pygame.display.update()

# Button: #

class Button():
	def __init__(self, display : pygame.Surface, x : int, y : int, image : pygame.Surface):
		self.display = display
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.buttonCooldown = 100
		self.buttonTimer = pygame.time.get_ticks()

	def render(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

				if(pygame.time.get_ticks() - self.buttonTimer >= self.buttonCooldown):

					action = True
					self.clicked = True
					self.buttonTimer = pygame.time.get_ticks()
			
		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False

		self.display.blit(self.image, (self.rect.x, self.rect.y))
		return action

	def changeButton(self, image : pygame.Surface):

		self.image = image

# Particles: #

class Particles():
	def __init__(self, game):

		# Game:

		self.game = game

		# Particle Groups:

		self.burnParticles = []
		self.runParticles = []
		self.jumpParticles = []


	def circleSurface(self, radius : int, color : tuple):
		surface = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surface, color, (radius, radius), radius)
		surface.set_colorkey((0, 0, 0))
		return surface

	def addGameParticle(self, particleType : str, x : int, y : int):
		particleType.lower()

		if(particleType == "lava"):
			self.burnParticles.append([[x, y], [0, -3], random.randint(12, 18)])

		elif(particleType == "run"):
			self.runParticles.append([[x + random.randint(-self.game.screenWidth // 80, self.game.screenWidth // 80), y], [random.randint(-4, 4), -0.5], random.randint(self.game.screenWidth // 1024, self.game.screenWidth // 512)])

		elif(particleType == "enemy"):
			self.runParticles.append([[x, y], [random.randint(-2, 2), -1], random.randint(1, 3)])

		elif(particleType == "jump"):
			self.jumpParticles.append([[x, y], [0, -2], random.randint(self.game.screenWidth // 256, self.game.screenWidth // 256)])

		else:
			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawGameParticles(self, particleType : str, color : tuple):

		if(particleType == "lava"):
			for particle in self.burnParticles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.game.display.blit(circleSurface(radius, color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				if(particle[2] <= 0):
					self.burnParticles.remove(particle)

		elif(particleType == "run"):
			for particle in self.runParticles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.05
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.runParticles.remove(particle)

		elif(particleType == "enemy"):
			for particle in self.runParticles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.runParticles.remove(particle)

		elif(particleType == "jump"):
			for particle in self.jumpParticles:
				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				if(particle[2] <= 0):
					self.jumpParticles.remove(particle)

		else:
			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawParticles(self):

		self.drawGameParticles("run", (255, 255, 255))
		self.drawGameParticles("jump", (160, 82, 45))

# Editor: #

class Editor():
	def __init__(self, game, world, assetsManager, menu):

		# Game:

		self.game = game

		# World:

		self.world = world
		self.worldGenerated = False

		# Assets Manager:

		self.assetsManager = assetsManager

		# Menu:

		self.menu = menu

		# Editor Settings:

		self.unsaved = False
		self.thisTile = 0

		# Tile Selection:

		self.editorTileSize = self.game.screenWidth // 42
		self.tileButtons = []
		self.tileColumn = 0
		self.tileRow = 0
		self.thisTile = 0

		# User Interface:

		self.interfaceReady = False
		self.buttonCount = 0
		self.sideMargin = pygame.Rect(self.game.screenWidth - self.game.screenWidth // 4, 0, self.game.screenWidth // 4, self.game.screenHeight)
		self.lowerMargin = pygame.Rect(0, self.game.screenHeight - self.game.screenHeight // 4, self.game.screenWidth, self.game.screenHeight // 4)
		
		# Buttons:

		self.saveButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 18), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Save"])
		self.clearButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 3), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Clear"])
		self.backButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 5), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Back"])

		# Timer:

		self.changeTimer = pygame.time.get_ticks()

		# Editor Tiles List:

		self.editorTiles = []

	def loadTiles(self):

		for tile in self.world.availableTiles:

			image = pygame.transform.scale(tile, (self.editorTileSize, self.editorTileSize))
			self.editorTiles.append(image)

	def loadNewLevel(self):

		with open(f'levels/level{self.game.level}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					self.world.worldData[x][y] = int(tile)

	def generateEditorWorld(self):

		if(not self.worldGenerated):

			for row in range(self.world.levelColumns):
				r = [-1] * self.world.levelColumns
				self.world.worldData.append(r)

			self.worldGenerated = True

	def drawGrid(self):

		for c in range(self.world.levelColumns + 1):
			pygame.draw.line(self.game.display, ((255, 255, 255)), (c * self.editorTileSize, 0), (c * self.editorTileSize, self.game.screenHeight))

		for c in range(self.world.levelRows + 1):
			pygame.draw.line(self.game.display, ((255, 255, 255)), (0, c * self.editorTileSize), (self.game.screenWidth, c * self.editorTileSize))

	def drawWorld(self):
		for y, row in enumerate(self.world.worldData):
			for x, tile in enumerate(row):
				if tile >= 0:
					self.game.display.blit(self.editorTiles[tile], (x * self.editorTileSize, y * self.editorTileSize))

	def drawUserInterface(self):

		pygame.draw.rect(self.game.display, ((140, 146, 172)), self.sideMargin)
		pygame.draw.rect(self.game.display, ((140, 146, 172)), self.lowerMargin)
		if(self.interfaceReady == False):

			for i in range(len(self.world.availableTiles)):
				tileButton = Button(self.game.display, self.game.screenWidth - ((self.game.screenWidth // 20) * self.tileColumn) - (self.game.screenWidth // 16), ((self.game.screenWidth // 25) * self.tileRow) + (self.game.screenHeight // 20), self.editorTiles[i])

				self.tileButtons.append(tileButton)
				self.tileColumn += 0.8
				if self.tileColumn == 4:
					self.tileRow += 0.8
					self.tileColumn = 0

			self.interfaceReady = True

		self.buttonCount = 0
		for self.buttonCount, button in enumerate(self.tileButtons):
			if button.render():
				self.thisTile = self.buttonCount

		for tile in range (len(self.tileButtons)):
			pygame.draw.rect(self.game.display, ((0, 0, 0)), self.tileButtons[tile].rect, self.game.screenWidth // 512)

		pygame.draw.rect(self.game.display, ((255, 0, 0)), self.tileButtons[self.thisTile].rect, self.game.screenWidth // 256)

	def drawInformation(self):

		if(self.unsaved):

			drawText(self.game.display, "Unsaved", self.game.screenWidth // 64, (255, 20, 10), self.game.screenWidth // 20, self.game.screenHeight - (self.game.screenHeight // 18))

		drawText(self.game.display, f"Level: {self.game.level}", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight - (self.game.screenHeight // 12))

	def handleButtons(self):
		i = 0
		if(self.saveButton.render() and self.unsaved):
			with open(f'levels/level{self.game.level}.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter = ',')
				for row in self.world.worldData:
					if(i >= self.world.levelRows):
						break
					writer.writerow(row)
					i += 1

			self.unsaved = False

		if(self.clearButton.render()):
			self.world.worldData = []

			for row in range(self.world.levelRows):

				r = [-1] * self.world.levelColumns
				self.world.worldData.append(r)

			for tile in range(0, self.world.levelColumns):

				self.world.worldData[self.world.levelRows - 1][tile] = 0

			self.unsaved = True

		if(self.backButton.render()):
			self.menu.mainMenu = True
			self.game.menuOn = True
			self.game.editorStatus = False
			self.world.setGameLevel(self.game.level)

	def handleEditor(self):

		position = pygame.mouse.get_pos()
		x = (position[0]) // self.editorTileSize
		y = position[1] // self.editorTileSize

		if(pygame.key.get_pressed()[pygame.K_z]):

			if(pygame.time.get_ticks() - self.changeTimer > 200 and self.game.level < 2):

				self.game.level += 1
				self.unsaved = False
				self.loadNewLevel()

		if(pygame.key.get_pressed()[pygame.K_s]):

			if(pygame.time.get_ticks() - self.changeTimer > 200 and self.game.level != 1):

				self.game.level -= 1
				self.unsaved = False
				self.loadNewLevel()

		if(position[0] < self.game.screenWidth and position[1] < self.game.screenHeight):

			if(not self.sideMargin.collidepoint(position) and not self.lowerMargin.collidepoint(position)):

				if (pygame.mouse.get_pressed()[0] == 1):

					if (self.world.worldData[y][x] != self.thisTile):

						self.world.worldData[y][x] = self.thisTile
						self.unsaved = True

				if (pygame.mouse.get_pressed()[2] == 1):

					if(not self.world.worldData[y][x] == -1):

						self.world.worldData[y][x] = -1
						self.unsaved = True
# Fade: #

class Fade():
	def __init__(self, game, direction : int, color : tuple):

		# Display: 

		self.game = game

		# Fade Settings: 

		self.direction = direction
		self.color = color
		self.speed = self.game.screenWidth // 128
		self.fadeCounter = 0
		self.fadeCompleted = False

	def reset(self):

		self.fadeCounter = 0
		self.fadeCompleted = False

	def fade(self):

		self.fadeCounter += self.speed

		if(self.direction == 1):

			pygame.draw.rect(self.game.display, self.color, (0 - self.fadeCounter, 0, self.game.screenWidth // 2, self.game.screenHeight))
			pygame.draw.rect(self.game.display, self.color, (self.game.screenWidth // 2 + self.fadeCounter, 0, self.game.screenWidth, self.game.screenHeight))
			pygame.draw.rect(self.game.display, self.color, (0, 0 - self.fadeCounter, self.game.screenWidth, self.game.screenHeight // 2))
			pygame.draw.rect(self.game.display, self.color, (0, self.game.screenHeight // 2 + self.fadeCounter, self.game.screenWidth, self.game.screenHeight))

		if(self.direction == 2):

			pygame.draw.rect(self.game.display, self.color, (0, 0, screenWidth, 0 + self.fadeCounter))
		
		if(self.fadeCounter >= self.game.screenWidth // 2):
			self.fadeCompleted = True

		return self.fadeCompleted