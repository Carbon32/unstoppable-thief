# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                       Unstoppable Thief, Level Editor                       #
#                             Developer: Carbon                   			  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import csv

# Pygame Initialization: #

pygame.init()

handleFPS = pygame.time.Clock()
FPS = 60

# Window Creation: #

screenWidth = 795
screenHeight = 795
lowerMargin = 200
sideMargin = 300

editorWindow = pygame.display.set_mode((screenWidth + sideMargin, screenHeight + lowerMargin))
pygame.display.set_caption('Unstoppable Thief: Level Editor')

# Editor Variables: #

editorRunning = True
editorRows = 15
editorColumns = 15
tileSize = screenHeight // editorRows
editorTiles = 13
level = 1
thisTile = 0

# Button Class:

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		editorWindow.blit(self.image, (self.rect.x, self.rect.y))
		return action


# Tile loading: #

tilesList = []
for c in range(1, editorTiles + 1):
	image = pygame.image.load(f'assets/Tiles/{c}.png').convert_alpha()
	image = pygame.transform.scale(image, (tileSize, tileSize))
	tilesList.append(image)

saveButton = pygame.image.load('assets/Save.png').convert_alpha()
loadButton = pygame.image.load('assets/Load.png').convert_alpha()
resetButton = pygame.image.load('assets/Reset.png').convert_alpha()
saveButton = pygame.transform.scale(saveButton, (saveButton.get_width() * 5, saveButton.get_height() * 5))
loadButton = pygame.transform.scale(loadButton, (loadButton.get_width() * 5, loadButton.get_height() * 5))
resetButton = pygame.transform.scale(resetButton, (resetButton.get_width() * 5, resetButton.get_height() * 5))

# Editor Font: #

font = pygame.font.SysFont('Impact', 15)

# Tile List: #

worldData = []
for row in range(editorRows):
	r = [-1] * editorColumns
	worldData.append(r)

# Ground Creation: #

for tile in range(0, editorColumns):
	worldData[editorRows - 1][tile] = 0


# Editor Text: #

def drawText(text, font, textColumn, x, y):
	image = font.render(text, True, textColumn)
	editorWindow.blit(image, (x, y))

# Draw Grid: #

def drawGrid():
	for c in range(editorColumns + 1):
		pygame.draw.line(editorWindow, ((255, 255, 255)), (c * tileSize, 0), (c * tileSize, screenHeight))

	for c in range(editorRows + 1):
		pygame.draw.line(editorWindow, ((255, 255, 255)), (0, c * tileSize), (screenWidth, c * tileSize))


# Draw World: #

def drawWorld():
	for y, row in enumerate(worldData):
		for x, tile in enumerate(row):
			if tile >= 0:
				editorWindow.blit(tilesList[tile], (x * tileSize, y * tileSize))

# Editor Buttons: #

buttonSave = Button(screenWidth // 2, screenHeight + lowerMargin - 120, saveButton, 1)
butttonLoad = Button(screenWidth // 2 + 200, screenHeight + lowerMargin - 120, loadButton, 1)
buttonReset = Button(screenWidth // 2 +  400, screenHeight + lowerMargin - 120, resetButton, 1)

buttonList = []
buttonColumn = 0
buttonRow = 0

for i in range(len(tilesList)):
	tileButton = Button(screenWidth + (75 * buttonColumn) + 50, 75 * buttonRow + 50, tilesList[i], 1)
	buttonList.append(tileButton)
	buttonColumn += 1
	if buttonColumn == 3:
		buttonRow += 1
		buttonColumn = 0


# Editor Loop: #

while editorRunning:

	handleFPS.tick(FPS)
	editorWindow.fill((100, 123, 255))
	drawGrid()
	drawWorld()

	drawText(f'Level: {level}', font, ((255, 255, 255)), 10, screenHeight + lowerMargin - 90)
	drawText('Press UP or DOWN to change level', font, ((255, 255, 255)), 10, screenHeight + lowerMargin - 60)

	# Save & Load:
	if buttonSave.draw():
		with open(f'levels/level{level}.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in worldData:
				writer.writerow(row)

	if butttonLoad.draw():
		with open(f'levels/level{level}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					worldData[x][y] = int(tile)

	if buttonReset.draw():
		worldData = []
		for row in range(editorRows):
			r = [-1] * editorColumns
			worldData.append(r)
		for tile in range(0, editorColumns):
			worldData[editorRows - 1][tile] = 0
				
	# Draw Tiles: 
	pygame.draw.rect(editorWindow, ((123, 15, 16)), (screenWidth, 0, sideMargin, screenHeight))

	# Choose Tile:
	buttonCount = 0
	for buttonCount, c in enumerate(buttonList):
		if c.draw():
			thisTile = buttonCount

	# Highlight: 
	pygame.draw.rect(editorWindow, ((255, 0, 0)), buttonList[thisTile].rect, 3)


	# Adding Tiles: 
	position = pygame.mouse.get_pos()
	x = (position[0]) // tileSize
	y = position[1] // tileSize

	if position[0] < screenWidth and position[1] < screenHeight:
		if pygame.mouse.get_pressed()[0] == 1:
			if worldData[y][x] != thisTile:
				worldData[y][x] = thisTile
		if pygame.mouse.get_pressed()[2] == 1:
			worldData[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			editorRunning = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1

	pygame.display.update()
pygame.quit()