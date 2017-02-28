import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0,128)

# Create a font object
fontObj = pygame.font.Font('freesansbold.ttf', 32)
# Render text onto a surface object, String of text, a boolean true for anti aliasing , text colour and backgroung color
textSurfaceObj = fontObj.render('Hello world!', True, GREEN, BLUE)
# Create a rectangle object with same height and width as text
textRectObj = textSurfaceObj.get_rect()
# Move the Rect center position
textRectObj.center = (200,150)

# Main game loop
while True:
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
