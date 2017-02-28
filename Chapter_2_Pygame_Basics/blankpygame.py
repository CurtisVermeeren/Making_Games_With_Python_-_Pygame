# Import pygame functions
import pygame, sys
from pygame.locals import *

# Needed to init pygame once modules are imported
pygame.init()
# Tell the window it's height and width
DISPLAYSURF = pygame.display.set_mode((400,300))
# Set the window text
pygame.display.set_caption('Hello World!')
# Main game loop
while True:
	# Get the list of event that have occured
	for event in pygame.event.get():
		# If there was a quit even found stop pygame and close the window
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	# Draw the surface object		
	pygame.display.update()
