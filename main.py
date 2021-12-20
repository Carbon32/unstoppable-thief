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

screenWidth = 1000
screenHeight = 1000

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Unstoppable Thief: ")

# Frame Limiter: #

handleFPS = pygame.time.Clock()
FPS = 60

# Game Variables: #

gameRunning = True
tileSize = 50

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
				if tile == 1:
					image = pygame.transform.scale(dirtTile, (tileSize, tileSize))
					imageRect = image.get_rect()
					imageRect.x = columnCount * tileSize
					imageRect.y = rowCount * tileSize
					tile = (image, imageRect)
					self.tileList.append(tile)
				columnCount += 1
			rowCount += 1

	def draw(self):
		for tile in self.tileList:
			gameWindow.blit(tile[0], tile[1])

class Player():
	def __init__(self, x, y):
		self.animationMove = []
		self.animationIdle = []
		self.index = 0
		self.animCounter = 0
		self.direction = 0
		for c in range(3):
			moveAnimation = pygame.image.load(f'assets/Player/Move/{c}.png')
			moveAnimation = pygame.transform.scale(moveAnimation, ((128, 128)))
			self.animationMove.append(moveAnimation)

			idleAnimation = pygame.image.load(f'assets/Player/Idle/{c}.png')
			idleAnimation = pygame.transform.scale(idleAnimation, ((128, 128)))
			self.animationIdle.append(idleAnimation)

		sprite = self.animationIdle[0]
		self.image = pygame.transform.scale(sprite, (128, 128))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.velocityY = 0
		self.alreadyJumped = False

	def update(self):
		# Movement:
		deltaX = 0
		deltaY = 0
		if(pygame.key.get_pressed()[pygame.K_q]):
			deltaX -= 5
			self.direction = 1
		if(pygame.key.get_pressed()[pygame.K_d]):
			deltaX += 5
			self.direction = 0
		if(pygame.key.get_pressed()[pygame.K_SPACE] and self.alreadyJumped == False):
			self.velocityY = -20
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

		# Gravity: 
		self.velocityY += 1
		if(self.velocityY > 10):
			self.velocityY = 10

		self.rect.x += deltaX
		self.rect.y += deltaY

		# Temporary Surface Limit: 
		if(self.rect.bottom > 950):
			self.rect.bottom = 950
			deltaY = 0

		# Draw Player:
		gameWindow.blit(self.image, self.rect)


# Game Mechanics: #

worldData = [ # Test Level: 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

world = World(worldData)
player = Player(100, 830)

# Game Loop: #

while(gameRunning):
	# Game Background: 
	gameWindow.fill((100, 123, 255))

	# FPS Handler: 
	handleFPS.tick(FPS)

	# Handle Game Mechanics:
	world.draw()
	player.update()


	# Event Handler: 
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	# Update Game Window: 
	pygame.display.update()

pygame.quit()