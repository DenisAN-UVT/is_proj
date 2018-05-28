import pygame
from constants import *
import boid
import model
import obstacle
import sys
from mesa import space

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

pygame.display.set_caption('Boids')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

# lists
boid_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.LayeredDirty()

my_model = model.BoidModel([background.get_width() // 2, background.get_height() //2], width=SCREEN_WIDTH, height=SCREEN_HEIGHT)


agents = my_model.schedule.agents

for a in agents:
    if isinstance(a, obstacle.Obstacle):
        obstacle_list.add(a)
    elif isinstance(a, boid.Boid):
        boid_list.add(a)
    all_sprites_list.add(a)

clock = pygame.time.Clock()
running = True

all_sprites_list.clear(screen, background)

while running:

    # --- events ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    text = "Boids Simulation with Obstacles: FPS: {0:.2f}".format(clock.get_fps())
    pygame.display.set_caption(text)

    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]

    # --- updates ---

    my_model.update_target([mouse_x, mouse_y])
    my_model.step()

    # Create list of dirty rects
    rects = all_sprites_list.draw(screen)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.update(rects)
    # Used to manage how fast the screen updates
    clock.tick(60)

# --- the end ---
pygame.quit()
sys.exit()

