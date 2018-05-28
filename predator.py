import numpy as np
import pygame
import sys

from mesa import Agent

from obstacle import Obstacle
import boid
from constants import *

class Predator(Agent, pygame.sprite.DirtySprite):


    def __init__(self, unique_id, model, pos, speed, velocity, vision, size,
                collision_separation, image):


        super().__init__(unique_id, model)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.collision_separation = collision_separation

    def attack(self, prey_neighbors):
        """

        :param prey_neighbors: prey to attack
        :return: vector in the direction of the attack
        """
        if not np.all(self.pos):
            print("fsfewf")
            sys.exit()
        attack_vector = np.zeros(2)
        if prey_neighbors:
            for p in prey_neighbors:
                attack_vector += self.model.space.get_heading(self.pos, p.pos)
            attack_vector /= len(prey_neighbors)
        return attack_vector

    def avoid_collision(self, objects):
        """
        :param objects: objects to avoid
        :return: a vector away from any objects closer than separation dist.
        """
        me = self.pos
        them = (obj.pos for obj in objects)
        avoidance_vector = np.zeros(2)
        for o in them:
            if self.model.space.get_distance(me, o) < self.collision_separation:
                avoidance_vector -= self.model.space.get_heading(me, o)
        return avoidance_vector

    def eat(self, prey_neighbors):
        if not prey_neighbors:
            return
        for p in prey_neighbors:
            if self.model.space.get_distance(self.pos, p.pos) < self.size:
                self.model.schedule.remove(p)
                self.model.space.remove_agent(p)
                p.dead = True



    # for drawing
    def update(self):
        self.rect.center = self.pos
        self.dirty = 1

    def step(self):
        """
        Get the Predator's neighbors, compute the new vector, and move accordingly.
        """
        prey_neighbors = [x for x in self.model.space.get_neighbors(self.pos, self.vision+ 20, False) if isinstance(x,boid.Boid)]
        nearby_obstacles = [x for x in self.model.space.get_neighbors(self.pos, self.vision + 15, False) if isinstance(x, Obstacle)]
        self.velocity += (self.avoid_collision(nearby_obstacles) * self.collision_separation +
                          self.attack(prey_neighbors)) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)
        self.eat(prey_neighbors)


        # update for drawing
        self.update()