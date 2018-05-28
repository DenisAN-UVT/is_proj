import numpy as np
import pygame

from mesa import Agent

from constants import *

class Obstacle(Agent, pygame.sprite.DirtySprite):
    def __init__(self, unique_id, model, pos, size):
        super().__init__(unique_id, model)
        pygame.sprite.DirtySprite.__init__(self)
        self.pos = pos
        # self.pos[0] += size//2
        # self.pos[1] += size//2

        self.image = pygame.Surface([size, size])
        if size > 5:
            self.image.fill(RED)
        else:
            self.image.fill(BLUE)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Coordinates
        if size > 5:
            self.rect.center = pos
        else:
            self.rect.center = pos



    def step(self):
        pass