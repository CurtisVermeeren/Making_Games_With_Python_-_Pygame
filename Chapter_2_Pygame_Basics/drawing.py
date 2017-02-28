import pygame, sys
from pygame.locals import *

pygame.init()

# Set up the window
DISPLAYSURF = pygame.display.set_mode ((500,400))
pygame.display.set_caption('Drawing')

# Set up colours
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Draw on the surface
# Fill the entire surface with a colour
DISPLAYSURF.fill(WHITE)

# Polgon draws lines between the points specified
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146,0), (291, 106), (236, 277), (56, 277), (0,106)))

# Draw lines with an optional list parameter
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)

# Draw a circle at the center point with radius 20 and width 0
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)

# Draw an ellipses given a bounding rectangle and with
pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)

# Draw a rectangle with a Tuple of 4 integers X and Y coordinates and height and width
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

# A pixel array object can be used to set individual pixel colours
pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
# Tell Pygame you are done drawing individual pixels by deleting the PixelArray
del pixObj

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
