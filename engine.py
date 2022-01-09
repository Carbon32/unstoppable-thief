# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Engine, Unstoppable Thief's Game Engine         #
#                                 Developer: Carbon               		      #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
from pygame import mixer
import csv
  
# Pygame Initialization: #

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Engine Variables: #
tileSize = 67
level = 1
maxLevels = 5
state = 0
coins = 0
jumpSound = mixer.Sound
arrestSound = mixer.Sound
coinSound = mixer.Sound
deathSound = mixer.Sound

# Groups: #
enemyGroup = pygame.sprite.Group()
lavaGroup = pygame.sprite.Group()
moneyGroup = pygame.sprite.Group()
coinGroup = pygame.sprite.Group()
platformGroup = pygame.sprite.Group()
playersGroup = pygame.sprite.Group()

# Engine Functions: #

def loadNextLevel(worldData : list):
	global level, state, maxLevels
	level += 1
	if(level > maxLevels):
		level = 1
	playersGroup.empty()
	enemyGroup.empty()
	lavaGroup.empty()
	moneyGroup.empty()
	coinGroup.empty()
	platformGroup.empty()
	for r in range(15):
		row = [-1] * 15
		worldData.append(row)

	with open(f'levels/level{level}.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for x, row in enumerate(reader):
			for y, tile in enumerate(row):
				worldData[x][y] = int(tile)
	state = 0
	return worldData

def setGameIcon(path : str):
	icon = pygame.image.load(path)
	pygame.display.set_icon(icon)

def checkGameState():
	return state

def playMusic(path : str, volume : int):
	pygame.mixer.music.load(path)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play(-1, 0.0, 5000)

def loadGameSound(path : str, volume : float):
	sound = pygame.mixer.Sound(path)
	sound.set_volume(volume)
	return sound

def assignGameSounds(coin : mixer.Sound, jump : mixer.Sound, arrest : mixer.Sound, death : mixer.Sound):
	global jumpSound, arrestSound, coinSound, deathSound
	jumpSound = jump
	arrestSound = arrest
	coinSound = coin
	deathSound = death

def resetLevel(worldData : list):
	global level, state, coins
	playersGroup.empty()
	enemyGroup.empty()
	lavaGroup.empty()
	moneyGroup.empty()
	coinGroup.empty()
	platformGroup.empty()
	for r in range(15):
		row = [-1] * 15
		worldData.append(row)

	with open(f'levels/level{level}.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for x, row in enumerate(reader):
			for y, tile in enumerate(row):
				worldData[x][y] = int(tile)
	state = 0
	coins = 0
	return worldData

def updateGameMechanics():
	enemyGroup.update()
	lavaGroup.update()
	moneyGroup.update()
	coinGroup.update()
	platformGroup.update()

def drawGameSprites(engineWindow : pygame.Surface, world : list):
	world.draw(engineWindow)
	drawStats(engineWindow)
	for player in playersGroup:
		player.draw(engineWindow, world)
	enemyGroup.draw(engineWindow)
	lavaGroup.draw(engineWindow)
	moneyGroup.draw(engineWindow)
	coinGroup.draw(engineWindow)
	platformGroup.draw(engineWindow)

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path)
		image = pygame.transform.scale(image, (width, height))
		return image

def loadStaticImage(path : str):
		image = pygame.image.load(path)
		return image

def assignWorldTiles():
	global level
	worldData = []
	for r in range(15):
		row = [-1] * 15
		worldData.append(row)

	with open(f'levels/level{level}.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for x, row in enumerate(reader):
			for y, tile in enumerate(row):
				worldData[x][y] = int(tile)
	return worldData

def drawText(engineWindow : pygame.Surface, text : str, color : tuple, size: int, x : int, y : int):
	image = pygame.font.SysFont('System', size).render(text, True, color)
	engineWindow.blit(image, (x, y))

def drawStats(engineWindow : pygame.Surface):
	global level, coins
	drawText(engineWindow, f'Coins: {coins}', (255, 255, 255), 30, 60, 20)
	drawText(engineWindow, f'Level: {level}', (255, 255, 255), 30, 400, 20)
	scoreCoin = Coin(tileSize // 2, tileSize // 2 - 5)
	coinGroup.add(scoreCoin)

def playerLost(world):
			world = resetLevel(level)
			gameOver = 0
			coins = 0

# Engine Window:

class Window():
	def __init__(self, screenWidth : int, screenHeight : int, windowTitle : str):
		global windowWidth, windowHeight
		windowWidth = screenWidth
		windowHeight = screenHeight
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.engineRunning = False
		self.windowTitle = windowTitle
		self.fpsLimit = pygame.time.Clock()
	
	def init(self):
		self.engineWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.windowTitle)
		self.engineRunning = True

	def quit(self):
		pygame.quit()

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False
		pygame.display.update()
		if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
			self.engineRunning = False

	def limitFPS(self, fps : int):
		self.fpsLimit.tick(fps)
	
	def setBackground(self, color : tuple):
		self.engineWindow.fill((color))

	def setMenuBackground(self, image : pygame.Surface):
		self.engineWindow.blit(image, (0, 0))

# World: #

class World():
	def __init__(self, data : list):
		global tileSize
		self.tileList = []
		# Load Tile:
		grassTile = pygame.image.load('assets/Tiles/grass.png')
		dirtTile = pygame.image.load('assets/Tiles/dirt.png')
		badDirtTile = pygame.image.load('assets/Tiles/bad_dirt.png')
		sandTile = pygame.image.load('assets/Tiles/sand.png')
		woodWall = pygame.image.load('assets/Tiles/wood_wall.png')
		shadow = pygame.image.load('assets/Tiles/shadow.png')

		# Select Tile:
		rowCount = 0
		for row in data:
			columnCount = 0 
			for tile in row:
				if(tile == 0): # Dirt: 
					image = pygame.transform.scale(dirtTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 1): # Grass:
					image = pygame.transform.scale(grassTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 2): # Bad Dirt:
					image = pygame.transform.scale(badDirtTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 3): # Sand: 
					image = pygame.transform.scale(sandTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 4): # Wooden Wall: 
					image = pygame.transform.scale(woodWall, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 5): # Shadow: 
					image = pygame.transform.scale(shadow, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)

				if(tile == 6): # Lava:
					lava = Lava(columnCount * tileSize, rowCount * tileSize + 34)
					lavaGroup.add(lava)

				if(tile == 7): # Enemy: 
					enemy = Enemy(columnCount * tileSize, rowCount * tileSize) 
					enemyGroup.add(enemy)

				if(tile == 8): # Money: 
					money = Money(columnCount * tileSize, rowCount * tileSize) 
					moneyGroup.add(money)

				if(tile == 9): # Coin: 
					coin = Coin(columnCount * tileSize + (tileSize // 2), rowCount * tileSize + (tileSize // 2)) 
					coinGroup.add(coin)

				if(tile == 10): # Platform (Left, right): 
					platform = Platform(columnCount * tileSize, rowCount * tileSize, True, False)
					platformGroup.add(platform) 

				if(tile == 11): # Platform (Up, down): 
					platform = Platform(columnCount * tileSize, rowCount * tileSize, False, True)
					platformGroup.add(platform) 

				if(tile == 12): # Player:
					player = Player(100, 830)
					playersGroup.add(player)
				columnCount += 1
			rowCount += 1


	def draw(self, engineWindow : pygame.Surface):
		for tile in self.tileList:
			engineWindow.blit(tile[0], tile[1])

# Platforms: #

class Platform(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int, moveX : bool, moveY : bool):
		global tileSize
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load('assets/Tiles/platform.png')
		self.image = pygame.transform.scale(image, (tileSize, tileSize // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.movementCounter = 0
		self.movementDirection = 1
		self.moveX = moveX
		self.moveY = moveY

	def update(self):
		self.rect.x += self.movementDirection * self.moveX
		self.rect.y += self.movementDirection *self.moveY
		self.movementCounter += 1
		if(abs(self.movementCounter) > 50):
			self.movementDirection *= -1
			self.movementCounter *= -1

# Player: #

class Player(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.reset(x, y)

	def draw(self, engineWindow : pygame.Surface, world : list):
		global state, coins
		# Movement:
		deltaX = 0
		deltaY = 0

		if(state == False):
			if(pygame.key.get_pressed()[pygame.K_q]):
				deltaX -= 5
				self.direction = 1
			if(pygame.key.get_pressed()[pygame.K_d]):
				deltaX += 5
				self.direction = 0
			if(pygame.key.get_pressed()[pygame.K_SPACE] and self.alreadyJumped == False and self.inAir == False):
				jumpSound.play()
				self.velocityY = -18
				self.alreadyJumped = True
			if(pygame.key.get_pressed()[pygame.K_SPACE] == False):
				self.alreadyJumped = False
			deltaY += self.velocityY


			# Handle Animation:
			coolDown = 5
			if(deltaX == 0):
				self.animCounter += 1
				if(self.animCounter > coolDown):
					self.animCounter = 0
					self.index += 1
					if(self.index >= len(self.animationIdle)):
						self.index = 0
					self.image = self.animationIdle[self.index]
					self.image = pygame.transform.flip(self.image, self.direction, False)
			else:
				self.animCounter += 1
				if(self.animCounter > coolDown):
					self.animCounter = 0
					self.index += 1
					if(self.index >= len(self.animationMove)):
						self.index = 0
					self.image = self.animationMove[self.index]
					self.image = pygame.transform.flip(self.image, self.direction, False)

			# Collision (To be improved):
			self.inAir = True
			for tile in world.tileList:
				if(tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.rect.width - 20, self.rect.height)):
					deltaX = 0

			for tile in world.tileList:
				if(tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.rect.width - 20, self.rect.height)):
					if(self.velocityY < 0):
						deltaY = tile[1].bottom - self.rect.top
						self.velocityY = 0

					elif(self.velocityY >= 0):
						deltaY = tile[1].top - self.rect.bottom
						self.velocityY = 0
						self.inAir = False

			if(pygame.sprite.spritecollide(self, coinGroup, True)):
				coinSound.play()
				coins += 1

			if(pygame.sprite.spritecollide(self, enemyGroup, False)):
				arrestSound.play()
				self.image = pygame.image.load('assets/Player/Arrest/0.png')
				self.image = pygame.transform.flip(self.image, self.direction, False)
				self.image = pygame.transform.scale(self.image, ((64, 64)))
				for enemy in enemyGroup:
					enemy.image = pygame.image.load('assets/Enemy/Arrest/0.png')
					enemy.image = pygame.transform.scale(enemy.image, ((64, 64)))
				state = -1

			if(pygame.sprite.spritecollide(self, lavaGroup, False)):
				deathSound.play()
				self.image = pygame.image.load('assets/Player/Dead/0.png')
				self.image = pygame.transform.flip(self.image, self.direction, False)
				self.image = pygame.transform.scale(self.image, ((64, 64)))
				state = -1

			if(pygame.sprite.spritecollide(self, moneyGroup, True)):
				state = 1

			thresh = 30
			for platform in platformGroup:
				if(platform.rect.colliderect(self.rect.x + deltaX, self.rect.y, self.rect.width - 20, self.rect.height)):
					deltaX = 0
				if(platform.rect.colliderect(self.rect.x, self.rect.y + deltaY, self.rect.width - 20, self.rect.height)):
					if abs((self.rect.top + deltaY) - platform.rect.bottom) < thresh:
						self.velocityY = 0
						deltaY = platform.rect.bottom - self.rect.top
					elif abs((self.rect.bottom + deltaY) - platform.rect.top) < thresh:
						self.rect.bottom = platform.rect.top
						deltaY = 0
						self.inAir = False
					if(platform.moveX == True):
						self.rect.x += platform.movementDirection
			# Gravity: 
			self.velocityY += 1
			if(self.velocityY > 20):
				self.velocityY = 20

			self.rect.x += deltaX
			self.rect.y += deltaY
		engineWindow.blit(self.image, self.rect)
		return state


	def reset(self, x : int, y : int):
		self.animationMove = []
		self.animationIdle = []
		self.index = 0
		self.animCounter = 0
		self.direction = 0
		for c in range(3):
			moveAnimation = pygame.image.load(f'assets/Player/Move/{c}.png')
			moveAnimation = pygame.transform.scale(moveAnimation, ((64, 64)))
			self.animationMove.append(moveAnimation)

			idleAnimation = pygame.image.load(f'assets/Player/Idle/{c}.png')
			idleAnimation = pygame.transform.scale(idleAnimation, ((64, 64)))
			self.animationIdle.append(idleAnimation)

		sprite = self.animationIdle[0]
		self.image = pygame.transform.scale(sprite, (64, 64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.velocityY = 0
		self.alreadyJumped = False
		self.inAir = True

# Enemy: #

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.enemyAnimations = []
		for c in range(3):
			enemyAnimation = pygame.image.load(f'assets/Enemy/Move/{c}.png')
			enemyAnimation = pygame.transform.scale(enemyAnimation, ((64, 64)))
			self.enemyAnimations.append(enemyAnimation)

		sprite = self.enemyAnimations[0]
		self.image = pygame.transform.scale(sprite, (64, 64))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.movementDirection = 1
		self.movementCounter = 0
		self.index = 0
		self.animCounter = 0

	def update(self):
		self.rect.x += self.movementDirection
		self.movementCounter += 1
		if abs((self.movementCounter > 50)):
			self.movementDirection *= -1
			self.movementCounter *= -1

		coolDown = 5
		self.animCounter += 1
		if(self.animCounter > coolDown):
			self.animCounter = 0
			self.index += 1
			if(self.index >= len(self.enemyAnimations)):
				self.index = 0
			self.image = self.enemyAnimations[self.index]
			self.image = pygame.transform.flip(self.image, self.movementDirection-1, False)

# Lava: #

class Lava(pygame.sprite.Sprite):
	global tileSize
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/Tiles/lava.png')
		self.image = pygame.transform.scale(self.image, (tileSize, tileSize // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Coins: #

class Coin(pygame.sprite.Sprite):
	global tileSize
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/Coins/coin.png')
		self.image = pygame.transform.scale(self.image, (tileSize // 2, tileSize // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

# Money Bag: #

class Money(pygame.sprite.Sprite):
	global tileSize
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/Tiles/money.png')
		self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Button: #

class Button():
	def __init__(self, x : int, y : int, image : pygame.Surface):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self, engineWindow : pygame.Surface):
		buttonClicked = False
		mousePosition = pygame.mouse.get_pos()
		if(self.rect.collidepoint(mousePosition)):
			if(pygame.mouse.get_pressed()[0] == True and self.clicked == False):
				buttonClicked = True
				self.clicked = True
		if(pygame.mouse.get_pressed()[0] == False):
			self.clicked = False

		engineWindow.blit(self.image, self.rect)
		return buttonClicked