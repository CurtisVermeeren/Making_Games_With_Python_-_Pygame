# Simulate Pygame

import random, sys, time, pygame
from pygame.locals import *

# Set fps, and window size
FPS = 30
WINDOWHEIGHT = 480
WINDOWWIDTH = 640
# The speed at which flashes are shown and the delay between them in miliseconds
FLASHSPEED = 500
FLASHDELAY = 200
# Button sizing
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
# The number of seconds before the game ends if no button pushed
TIMEOUT = 4

# Define RGB colors
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

# Calculate margins around the board
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Use Rect objects for the 4 buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT  = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

# Main function
def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Simulate Game')

	BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

	# Create info text and surface
	infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
	inforRect = infoSurf.get_rect()
	inforRect.topleft = (10, WINDOWHEIGHT - 25)

	# Load the sound files
	BEEP1 = pygame.mixer.Sound('beep1.ogg')
	BEEP2 = pygame.mixer.Sound('beep2.ogg')
	BEEP3 = pygame.mixer.Sound('beep3.ogg')
	BEEP4 = pygame.mixer.Sound('beep4.ogg')

	# Stores the pattern of colors
	pattern = []
	# The color the player must press next
	currentStep = 0
	# The time of the player's last button push
	lastClickTime = 0
	score = 0
	# False = pattern is playing, True = waiting for the player to input
	waitingForInput = False

	# Main game loop
	while True:
		# The button that was clicked
		clickedButton = None

		DISPLAYSURF.fill(bgColor)
		drawButtons()

		# Create a surface to display the score
		# Will be updated so it will be recreated in the loop
		scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WINDOWWIDTH - 100, 10)
		DISPLAYSURF.blit(scoreSurf, scoreRect)

		DISPLAYSURF.blit(infoSurf, inforRect)

		# Check for mouse clicks and keyboard presses in the event loop
		checkForQuit()
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				# The the position of the mouse and buttons clicked if any
				mousex, mousey = event.pos
				clickedButton = getButtonClicked(mousex,mousey)
			elif event.type == KEYDOWN:
				# Associate the 4 buttons with 4 different keys
				if event.key == K_q:
					clickedButton = YELLOW
				elif event.key == K_w:
					clickedButton = BLUE
				elif event.key == K_a:
					clickedButton = RED
				elif event.key == K_s:
					clickedButton = GREEN

		# If not waiting for input play the pattern
		if not waitingForInput:
			pygame.display.update()
			pygame.time.wait(1000)
			# Add a random color to the pattern
			pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
			# Flash each button using the animation
			for button in pattern:
				flashButtonAnimation(button)
				pygame.time.wait(FLASHDELAY)
			waitingForInput = True
		# Wait for the player to click buttons
		else :
			# Pressed the correct button
			if clickedButton and clickedButton == pattern[currentStep]:
				flashButtonAnimation(clickedButton)
				currentStep += 1
				lastClickTime = time.time()
				# Check if this was the last button in the pattern
				if currentStep == len(pattern):
					# Reset the game
					changeBackgroundAnimation()
					score += 1
					waitingForInput = False
					currentStep = 0
			# The wrong button was pressed or too much time has passed
			elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
				gameOverAnimation()
				# Reset for a new game
				pattern = []
				currentStep = 0
				waitingForInput = False
				score = 0
				pygame.time.wait(1000)
				changeBackgroundAnimation()

		# Draw the board to the screen
		pygame.display.update()
		FPSCLOCK.tick(FPS)

# Functions to terminate the program and check for quit events
def terminate():
	pygame.quit()
	sys.exit()

def checkForQuit():
	for event in pygame.event.get(QUIT):
		terminate()
	for event in pygame.event.get(KEYUP):
		if event.key == L_ESCAPE:
			terminate()
		pygame.event.post(event)

def flashButtonAnimation(color, animationSpeed=50):
	# Set the sound, color, and rectangle depening on the button
	if color == YELLOW:
		sound = BEEP1
		flashColor = BRIGHTYELLOW
		rectangle = YELLOWRECT
	if color == BLUE:
		sound = BEEP2
		flashColor = BRIGHTBLUE
		rectangle = BLUERECT
	if color == RED:
		sound = BEEP3
		flashColor = BRIGHTRED
		rectangle = REDRECT
	if color == GREEN:
		sound = BEEP4
		flashColor = BRIGHTGREEN
		rectangle = GREENRECT
	# On each frame the normal board is drawn with bright coloured flashing button on topleft
	# Alpha value begines as 0 then sloly increases to make the button look like it's brightening
	origSurf = DISPLAYSURF.copy()
	flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
	# Convert alpha used so the surface object can have transparent colors drawn on it
	flashSurf = flashSurf.convert_alpha()
	r, g, b = flashColor
	sound.play()
	# The animation loop
	for start, end, step in ((0, 255, 1), (255, 0, -1)):
		for alpha in range(start, end, animationSpeed * step):
			checkForQuit()
			DISPLAYSURF.blit(origSurf, (0, 0))
			flashSurf.fill((r, g, b, alpha))
			DISPLAYSURF.blit(flashSurf, rectangle.topleft)
			pygame.display.update()
			# Add short pauses with tick to ensure frames aren't drawn as soon as possible
			FPSCLOCK.tick(FPS)
	DISPLAYSURF.blit(origSurf, (0, 0))

# Function to draw the buttons
def drawButtons():
	pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
	pygame.draw.rect(DISPLAYSURF, BLUE,   BLUERECT)
	pygame.draw.rect(DISPLAYSURF, RED,    REDRECT)
	pygame.draw.rect(DISPLAYSURF, GREEN,  GREENRECT)

# Function to animate the background changing
def changeBackgroundAnimation(animationSpeed=40):
	global bgColor
	newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
	newBgSurf = newBgSurf.convert_alpha()
	r, g, b = newBgColor
	# The animation loop
	for alpha in range(0, 255, animationSpeed):
		checkForQuit()
		DISPLAYSURF.fill(bgColor)

		newBgSurf.fill((r, g, b, alpha))
		DISPLAYSURF.blit(newBgSurf, (0, 0))

		# Redraw the buttons on top
		drawButtons()

		pygame.display.update()
		FPSCLOCK.tick(FPS)
	bgColor = newBgColor

# Function for the game over animation
def gameOverAnimation(color=WHITE, animationSpeed=50):
	# Play all beeps at once then flash the background
	origSurf = DISPLAYSURF.copy()
	flashSurf = pygame.Surface(DISPLAYSURF.get_size())
	flashSurf = flashSurf.convert_alpha()
	BEEP1.play()
	BEEP2.play()
	BEEP3.play()
	BEEP4.play()
	r,g,b = color
	# Do the flash 3 times
	for i in range(3):
		for start, end, step in ((0, 255, 1), (255, 0, -1)):
			for alpha in range(start, end, animationSpeed * step):
				checkForQuit()
				flashSurf.fill((r, g, b, alpha))
				DISPLAYSURF.blit(origSurf, (0, 0))
				DISPLAYSURF.blit(flashSurf, (0, 0))
				drawButtons()
				pygame.display.update()
				FPSCLOCK.tick(FPS)

# Function to get pixel coordinates to buttons
def getButtonClicked(x, y):
	if YELLOWRECT.collidepoint((x, y)):
		return YELLOW
	elif BLUERECT.collidepoint( (x, y) ):
		return BLUE
	elif REDRECT.collidepoint( (x, y) ):
		return RED
	elif GREENRECT.collidepoint( (x, y) ):
		return GREEN

if __name__ == '__main__':
	main()
