# Wormy created in Pygame

import random, pygame, sys
from pygame.locals import *

# Set up window and cells
FPS = 15
WINDOWHEIGHT = 480
WINDOWWIDTH = 640
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Create colors
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

# Create direction objects
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Index to track the worm's head use worm[HEAD] instead of worm[0]
HEAD = 0

# Main Function
def main():
	# Initalize game
	global FPSCLOCK, DISPLAYSURF, BASICFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Wormy!')
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

	# Show the start screen
	showStartScreen()
	# Main game loop
	while True:
		# Run the game function
		runGame()
		# When game function returns the player has lost
		showGameOverScreen()

# Function to run the game
def runGame():
	# Find a random point to start at that the worm will fit
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	# Set the worms coordinates one entry per worm segment
	wormCoords = [{'x': startx, 'y': starty},
				  {'x': startx-1, 'y':starty},
				  {'x': startx-2, 'y':starty}]
	# The direction the worm is facing
	direction = RIGHT
	# Start the apple pickup in a random spot
	apple = getRandomLocation()

	# Main game loop
	while True:
		# Event handling loop
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				# The worm can only left or right of it's current direction not a U-turn
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()

		# Check if the worm has it the edge or itself
		if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
			# Return which will run game over
			return
		for wormBody in wormCoords[1:]:
			# If the head of the worm has hit one of it's body parts
			if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
				return

		# Check if the worm has eaten an apple
		if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
			# Set a new apple somewhere
			apple = getRandomLocation()
		else:
			# If an apple hasn't beern eaten remove the tail
			del wormCoords[-1]

		# Move the worm by adding a segment in the direction it is moving
		if direction == UP:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
		# Add the new head in front of the old one
		wormCoords.insert(0, newHead)

		# Drawing the screen
		DISPLAYSURF.fill (BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(len(wormCoords) - 3)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

# Function to print a message
def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

# Function checks for key presses
def checkForKeyPress():
	# If there are any quit events then leave
	if len(pygame.event.get(QUIT)) > 0:
		terminate()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key

# Function to show the start screen
def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
	titleSurf2 = titleFont.render('Wormy!', True, GREEN)

	degrees1 = 0
	degrees2 = 0
	# Animation Loop
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

		drawPressKeyMsg()

		if checkForKeyPress():
			pygame.event.get()
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		degrees1 += 3 # rotate by 3 degrees each frame
		degrees2 += 7 # rotate by 7 degrees each frame

# Function to terminate the program
def terminate():
	pygame.quit()
	sys.exit()

# Function to get a random location
def getRandomLocation():
	return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

# Function to show the game over animation
def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	gameRect.midtop = (WINDOWWIDTH / 2, 10)
	overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

	DISPLAYSURF.blit(gameSurf, gameRect)
	DISPLAYSURF.blit(overSurf, overRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()
	# Game over text will stay on screen until a key is pressed
	while True:
		if checkForKeyPress():
			pygame.event.get()
			return

# Function to draw the score
def drawScore(score):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 120, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

# Function to draw the worm
def drawWorm(wormCoords):
	# Draw each segment
	for coord in wormCoords:
		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
		pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
		# Draw a smaller rect inside to give the worm style
		wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE-8, CELLSIZE-8)
		pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

# Function to draw an apple
def drawApple(coord):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
	pygame.draw.rect(DISPLAYSURF, RED, appleRect)

# Function to draw the grid lines
def drawGrid():
	for x in range(0, WINDOWWIDTH, CELLSIZE):
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELLSIZE):
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
	main()
