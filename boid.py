import sys

import numpy as np
import pygame

from mesa import Agent
from obstacle import Obstacle
from predator import Predator
from constants import *


class Boid(Agent, pygame.sprite.DirtySprite):
    """
    A Boid-style flocker agent.

    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents.
        - Separation: avoiding getting too close to any other agent.
        - Alignment: try to fly in the same direction as the neighbors.

    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(self, unique_id, model, pos, speed, velocity, vision,
                 separation, collision_separation, image, size, cohere=0.025, separate=0.25, match=0.04):
        """
        :param unique_id: Unique agent identifier
        :param model: model
        :param pos: Starting position
        :param speed: Distance to move per step
        :param velocity: vector for direction of movement
        :param vision: distance to look for neighbouring agents
        :param separation: minimum distance to maintain from other boid agents
        :param collision_separation: minimum distance to maintain from obstacle agents
        :param image: image path used for pygame
        :param cohere: the relative importance of matching neighbors' positions
        :param separate: the relative importance of avoiding close neighbors
        :param match: the relative importance of matching neighbors' headings
        """
        super().__init__(unique_id, model)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.collision_separation = collision_separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match
        self.dead = False

    def cohere(self, neighbors):
        """

        :param neighbors: neighbouring boids
        :return:  the vector toward the center of mass of the local neighbors.
        """
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        """

        :param neighbors: neighbouring boids
        :return: a vector away from any neighbors closer than separation dist.
        """
        me = self.pos
        them = (n.pos for n in neighbors)
        separation_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation + self.size:
                separation_vector -= self.model.space.get_heading(me, other)
        return separation_vector

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

    def match_heading(self, neighbors):
        """
        :param neighbors:
        :return: a vector of the neighbors' average heading.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
            # print(match_vector)
        return match_vector

    def move_towards_target(self, target):
        """

        :param target: set of coordinates to move towards
        :return: a vector of movement towards the target
        """
        move_vector = np.zeros(2)

        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        distance = self.model.space.get_distance(self.pos, target)

        dx /= distance
        dy /= distance

        move_vector[0] += dx
        move_vector[1] += dy

        return move_vector

    # for drawing
    def update(self):
        self.rect.center = self.pos
        self.dirty = 1

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """
        if not np.any(self.pos):
            return
        neighbors = [x for x in self.model.space.get_neighbors(self.pos, self.vision + self.size, False) if isinstance(x,Boid)]
        nearby_obstacles = [x for x in self.model.space.get_neighbors(self.pos, self.vision + 15, False) if isinstance(x, Obstacle)]
        predator_neighbors = [x for x in self.model.space.get_neighbors(self.pos, self.vision + self.size, False) if isinstance(x, Predator)]
        self.velocity += (self.cohere(neighbors) * self.cohere_factor +
                          self.separate(neighbors) * self.separate_factor +
                          self.avoid_collision(predator_neighbors) +
                          self.avoid_collision(nearby_obstacles) +
                          self.match_heading(neighbors) )
        if(self.model.mouse):
            self.velocity += self.move_towards_target(self.model.target)
        self.velocity /= 2
        self.velocity /= np.linalg.norm(self.velocity)
        if len(neighbors) == 1:
            print(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)

        # update for drawing
        self.update()
