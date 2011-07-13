#!/usr/bin/env python
'''
Module includes various game objects.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame
import pygame.locals as pyg_loc

import math
import logging
import colorer
LOGGER = logging.getLogger('main.gameobjects')

import Box2D as box2d

import data

FILL_COLOR = pygame.Color(125, 255, 125, 0)
BORDER_COLOR = pygame.Color(0, 0, 255, 255)

class GameObject(pygame.sprite.Sprite):
    '''Class, representing base game object. Subject of derivation of other,
    more specific game objects.'''

    def __init__(self, scale, pos, image, size):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.position = list(pos)
        if isinstance(image, str):
            self.image = data.load_image(image, -1)
        else:
            self.image = image
        size = self.transform(size)
        self.image = pygame.transform.scale(self.image, map(int, size)).convert()
        self.original_img = self.image
        self.rect = self.image.get_rect()

    def transform(self, point):
        return point[0] * self.scale[0], point[1] * self.scale[1]

    def apply_force(self, x, y):
        mass = self.physics.GetMass()
        mass_center = self.physics.GetWorldCenter()
        self.physics.ApplyForce(box2d.b2Vec2(x * mass, y * mass), mass_center)

    def apply_impulse(self, x, y):
        mass_center = self.physics.GetWorldCenter()
        self.physics.ApplyImpulse(box2d.b2Vec2(x, y), mass_center)           

class Ball(GameObject):
    '''Round object.'''

    def __init__(self, world, scale=(1, 1), radius=1, pos=(5, 5), dynamic=True):
        GameObject.__init__(self, scale, pos, 'Hairy_Ball.png', (radius * 2, radius * 2))
        self.radius = radius
        self.physics = self.create_phisycs_object(world, dynamic)

    def create_phisycs_object(self, world, dynamic):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (self.position[0] + self.radius / 2, self.position[1] + self.radius / 2)
        bodyDef.userdata = self
        body = world.CreateBody(bodyDef)
        shapeDef = box2d.b2CircleDef()
        shapeDef.radius = self.radius
        if dynamic:
            shapeDef.density = 1
        shapeDef.linearDamping = 0.0
        shapeDef.angularDamping = 0.0
        shapeDef.friction = 0.1
        shapeDef.restitution = 1
        body.CreateShape(shapeDef)
        body.SetMassFromShapes()
        return body

    def update(self):
        angle = -self.physics.angle * 180 / math.pi
        self.image = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.image.get_rect()
        self.position = self.transform(self.physics.position.tuple())
        self.rect.center = self.position

    
class Box(GameObject):
    '''Rectangular objects.'''

    def __init__(self, world, scale=(1, 1), size=(1, 1), pos=(5, 5), dynamic=True):
        surface = pygame.Surface((size[0] * scale[0], size[1] * scale[1]))
        surface.fill(FILL_COLOR)
        surface.set_colorkey(FILL_COLOR, pyg_loc.RLEACCEL)
        draw_AABB(surface, (size[0], size[1]), scale, BORDER_COLOR)

        GameObject.__init__(self, scale, pos, surface, size)
        self.size = size
        self.physics = self.create_phisycs_object(world, dynamic)

    def create_phisycs_object(self, world, dynamic):
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
        bodyDef.userdata = self
        body = world.CreateBody(bodyDef)
        shapeDef = box2d.b2PolygonDef()
        shapeDef.SetAsBox(self.size[0] / 2, self.size[1] / 2)
        if dynamic:
            shapeDef.density = 1
        shapeDef.linearDamping = 0.0
        shapeDef.angularDamping = 0.0
        shapeDef.friction = 0.1
        shapeDef.restitution = 1
        body.CreateShape(shapeDef)
        body.SetMassFromShapes()
        return body

    def update(self):
        angle = -self.physics.angle * 180 / math.pi
        self.image = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.image.get_rect()
        self.position = self.transform(self.physics.position.tuple())
        self.rect.center = self.position


def draw_AABB(surface, (w, h), scale, color):
    """
    Draw a wireframe around the AABB with the given color.
    """
    points = [  (1, 1),
                (w * scale[0] - 2, 1),
                (w * scale[0] - 2, h * scale[1] - 2),
                (1, h * scale[1] - 2),
            ]

    pygame.draw.aalines(surface, color, True, points)
