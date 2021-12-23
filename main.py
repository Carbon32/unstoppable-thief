# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Unstoppable Thief, platformer video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame

# Pygame Initialization: #

pygame.init()

# Game Window: #

screenWidth, screenHeight = 1000, 1000

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Unstoppable Thief: ")

# Frame Limiter: #

handleFPS = pygame.time.Clock()
FPS = 60

# Game Variables: #

gameRunning = True
tileSize = screenHeight // 15
gameOver = False
mainMenu = True

# Game Button: #

restartImage = pygame.image.load('assets/Buttons/restart.png')
startImage = pygame.image.load('assets/Buttons/start.png')
exitImage = pygame.image.load('assets/Buttons/exit.png')

# Game Classes: #

class World():
	def __init__(self, data):
		self.tileList = []
		# Load Tile:
		grassTile = pygame.image.load('assets/Tiles/grass.png')
		dirtTile = pygame.image.load('assets/Tiles/dirt.png')
		badDirtTile = pygame.image.load('assets/Tiles/bad_dirt.png')
		sandTile = pygame.image.load('assets/Tiles/sand.png')

		# Select Tile:
		rowCount = 0
		for row in data:
			columnCount = 0 
			for tile in row:
				if(tile == 1): # Dirt: 
					image = pygame.transform.scale(dirtTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)
				if(tile == 2): # Grass:
					image = pygame.transform.scale(grassTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)
				if(tile == 3): # Bad Dirt:
					image = pygame.transform.scale(badDirtTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)
				if(tile == 4): # Sand: 
					image = pygame.transform.scale(sandTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)
				if(tile == 5): # Lava:
					lava = Lava(columnCount * tileSize, rowCount * tileSize + 34)
					lavaGroup.add(lava)
				if(tile == 6): # Enemy: 
					enemy = Enemy(columnCount * tileSize, rowCount * tileSize) 
					enemyGroup.add(enemy)
				columnCount += 1
			rowCount += 1


	def draw(self):
		for tile in self.tileList:
			gameWindow.blit(tile[0], tile[1])

class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, state):
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
				self.velocityY = -15
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

			if(pygame.sprite.spritecollide(self, enemyGroup, False)):
				self.image = pygame.image.load('assets/Player/Arrest/0.png')
				self.image = pygame.transform.flip(self.image, self.direction, False)
				self.image = pygame.transform.scale(self.image, ((64, 64)))
				state = True

			if(pygame.sprite.spritecollide(self, lavaGroup, False)):
				self.image = pygame.image.load('assets/Player/Dead/0.png')
				self.image = pygame.transform.flip(self.image, self.direction, False)
				self.image = pygame.transform.scale(self.image, ((64, 64)))
				state = True

			# Gravity: 
			self.velocityY += 1
			if(self.velocityY > 20):
				self.velocityY = 20

			self.rect.x += deltaX
			self.rect.y += deltaY

		# Draw Player:
		gameWindow.blit(self.image, self.rect)

		# Return Game State:
		return state

	def reset(self, x, y):
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


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
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

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('assets/Tiles/lava.png')
		self.image = pygame.transform.scale(self.image, (tileSize, tileSize // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		buttonClicked = False
		mousePosition = pygame.mouse.get_pos()
		if(self.rect.collidepoint(mousePosition)):
			if(pygame.mouse.get_pressed()[0] == True and self.clicked == False):
				buttonClicked = True
				self.clicked = True
		if(pygame.mouse.get_pressed()[0] == False):
			self.clicked = False

		gameWindow.blit(self.image, self.rect)
		return buttonClicked


# Game Mechanics: #

worldData = [ # Test Level: 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Groups:
enemyGroup = pygame.sprite.Group()
lavaGroup = pygame.sprite.Group()

# Game Instances: 
world = World(worldData)
player = Player(20, 830)

# Buttons: 
restartButton = Button(screenWidth // 2 - 120, screenHeight // 2 - 200, restartImage)
startButton = Button(screenWidth // 2 - 120, screenHeight // 2 - 200, startImage)
exitButton = Button(screenWidth // 2 - 120, screenHeight // 2, exitImage)

# Game Loop: #

while(gameRunning):
	# Game Background: 
	gameWindow.fill((100, 123, 255))

	# FPS Handler: 
	handleFPS.tick(FPS)

	# Main Menu:
	if(mainMenu == True):
		if(startButton.draw()):
			mainMenu = False
		if(exitButton.draw()):
			gameRunning = False

	else:
		# Handle Game Mechanics:
		world.draw()
		gameOver = player.update(gameOver)
		if(gameOver == True):
			if(restartButton.draw()):
				player.reset(20, 830)
				gameOver = False
		if(gameOver == False):
			enemyGroup.update()
		else:
			for enemy in enemyGroup:
				enemy.image = pygame.image.load('assets/Enemy/Arrest/0.png')
				enemy.image = pygame.transform.flip(enemy.image, enemy.movementDirection-1, False)
				enemy.image = pygame.transform.scale(enemy.image, ((64, 64)))

		enemyGroup.draw(gameWindow)
		lavaGroup.draw(gameWindow)


	# Event Handler: 
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	# Update Game Window: 
	pygame.display.update()

pygame.quit()