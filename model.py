'''
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
'''

import random
import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from boid import Boid
from obstacle import Obstacle
from predator import Predator


class BoidModel(Model):
    '''
    Flocker model class. Handles agent creation, placement and scheduling.
    '''

    def __init__(self,
                 target,
                 predators=False,
                 mouse=True,
                 population=50,
                 width=100,
                 height=100,
                 speed=2,
                 vision=10,
                 separation=1,
                 collision_separation=30,
                 cohere=0.05,
                 separate=1.25,
                 match=0.4):
        '''
        Create a new Flockers model.

        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives.        '''
        self.target = target
        self.predators = predators
        self.mouse = mouse
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.collision_separation = collision_separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True

    def update_target(self, target):
        self.target = target

    def make_agents(self):
        '''
        Create self.population agents, with random positions and starting headings.
        '''
        for i in range(50):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            center_x = self.space.x_max/2
            center_y = self.space.y_max/2
            pos = np.array((x, y))
            center = np.array((center_x,center_y))
            velocity = np.random.random(2) * 2 - 1
            velocity = np.zeros(2) + self.space.get_distance(pos, center)
            velocity[0] *= self.target[0]
            velocity[1] *= self.target[1]
            boid = Boid(i, self, pos, self.speed, velocity, self.vision,
                        self.separation, self.collision_separation, "boid.png", 10, **self.factors)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

        for i in range(4):
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = np.array((x, y))
            obstacle = Obstacle(i + self.population, self, pos, 30)
            obstacle2 = Obstacle(i + self.population + 5, self, pos, 4)
            self.space.place_agent(obstacle, pos)
            self.space.place_agent(obstacle2,pos)
            self.schedule.add(obstacle)
            self.schedule.add(obstacle2)
        if self.predators:
            x = random.random() * self.space.x_max
            y = random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            predator = Predator(2003,self, pos, self.speed + 0.1, velocity, self.vision + 5, 12, self.collision_separation, "predator.png")
            self.space.place_agent(predator,pos)
            self.schedule.add(predator)

    def step(self):
        self.schedule.step()
