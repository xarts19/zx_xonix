#!/usr/bin/env python
'''
Module includes ...(something, not yet sure) that process and renders velocities 
and positions of game objects.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import logging
import colorer
LOGGER = logging.getLogger('main.physicsengine')

import Box2D as box2d

import gameobjects
import data

class Simulation():

    def __init__(self, screen_size, real_size):
        self._scr_size = screen_size
        self._real_size = real_size
        scale_x = screen_size[0] / float(real_size[0])
        scale_y = screen_size[1] / float(real_size[1])
        self.scale = scale_x, scale_y
        self.world = self.create_physics_world(real_size)
        self.static_objects = []
        self.dynamic_objects = []

        self.timeStep = 1.0 / 60.0
        self.velocity_iterations = 10
        self.position_iterations = 8

    def get_objects(self):
        return self.static_objects + self.dynamic_objects

    def create_level(self, level=0):
        '''Loads level specifications and populate world with appropriate static boxes'''
        if data.LEVELS.get(level):
            for pos, size in data.LEVELS[level]:
                self.create_box(pos, size, False)
        else:
            raise(Exception("No such level: {0}".format(level)))

    def create_physics_world(self, size):
        # create world
        worldAABB = box2d.b2AABB()
        worldAABB.lowerBound = (-10, -10)
        worldAABB.upperBound = (size[0] + 10, size[1] + 10)
        gravity = box2d.b2Vec2(0.0, 0.0)
        doSleep = True
        world = box2d.b2World(worldAABB, gravity, doSleep)
        return world

    def create_box(self, pos, size, dynamic=True):
        box = gameobjects.Box(self.world, self.scale, size, pos, dynamic)
        if dynamic:
            self.dynamic_objects.append(box)
        else:
            self.static_objects.append(box)
        return box

    def create_ball(self, pos, radius, dynamic=True):
        ball = gameobjects.Ball(self.world, self.scale, radius, pos, dynamic)
        if dynamic:
            self.dynamic_objects.append(ball)
        else:
            self.static_objects.append(ball)
        return ball

    def step(self):
        self.world.Step(self.timeStep, self.velocity_iterations, self.position_iterations)

    def applyGravity(self, x, y):
        self.world.SetGravity(box2d.b2Vec2(x, y))
        for body in self.world:
            body.WakeUp()
