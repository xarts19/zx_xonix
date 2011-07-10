#!/usr/bin/env python
'''
Module includes various game objects.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame

import math
import logging
import colorer
LOGGER = logging.getLogger('main.gameobjects')

import Box2D as box2d

import data

class GameObject(pygame.sprite.Sprite):
    '''Class, representing base game object. Subject of derivation of other,
    more specific game objects.'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



class Ball(GameObject):
    '''Round object.'''

    def __init__(self, world, world_scale, radius=1, pos=(5, 5)):
        GameObject.__init__(self)
        self.scale = world_scale
        self.radius = radius
        self.position = list(pos)
        self.speed = (0, 0)
        self.physics = self.create_phisycs_object(world)
        self.image, self.rect = data.load_image('ball.gif', -1)
        size = self.transform((self.radius * 2, self.radius * 2))
        self.image = pygame.transform.scale(self.image, size).convert()
        self.original_img = self.image
        self.rect = self.image.get_rect()

    def create_phisycs_object(self, world):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = self.position
        bodyDef.userdata = self
        bodyDef.massData.mass = 0.01
        body = world.CreateBody(bodyDef)
        shapeDef = box2d.b2CircleDef()
        shapeDef.radius = self.radius
        shapeDef.density = 1
        shapeDef.friction = 0.5
        body.CreateShape(shapeDef)
        body.SetMassFromShapes()
        return body

    def update(self):
        angle = -self.physics.angle * 180 / math.pi
        self.image = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.image.get_rect()
        self.position = self.transform(self.physics.position.tuple())
        self.rect.center = self.position


    def update_speed(self, speed):
        self.speed = speed

    def transform(self, point):
        return point[0] * self.scale[0], point[1] * self.scale[1]

