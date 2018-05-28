import pygame

pygame.init()
flags = pygame.DOUBLEBUF
# === constants ===

infoObject = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000,900
pygame.quit()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)

MAX_BOID_VELOCITY = 1
NUM_BOIDS = 55
NUM_PREY = 70
NUM_PREDATORS = 5
MAX_PREY_VELOCITY = 1
MAX_PREDATOR_VELOCITY = 1.5
NUM_OBSTACLES = 17
BORDER = 30
FIELD_OF_VIEW = 70
