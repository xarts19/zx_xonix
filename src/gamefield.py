#!/usr/bin/env python
'''
Module will include GameField class and various utility functions for working with it.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame

import math
import parser
import logging
import colorer
LOGGER = logging.getLogger('main.gamefield')

import Box2D as box2d

BORDER_COLOR = pygame.Color(0, 0, 255, 255)

class GameField(pygame.sprite.Sprite):
    '''Represents a game field as a set of inequalities.'''

    def __init__(self, scale=(6, 6), size=(100, 100), level=1):
        self.scale = scale
        self.size = size[0] * scale[0], size[1] * scale[1]
        self.world_size = size

        surface = pygame.Surface(self.size)
        surface.fill((125, 255, 125, 255))

        self.world = self.create_physics_object(surface)

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(surface, self.size).convert()
        self.rect = self.image.get_rect()   # Rect area for updating image

    def create_physics_object(self, surface):
        # create world
        worldAABB = box2d.b2AABB()
        worldAABB.lowerBound = (-10, -10)
        worldAABB.upperBound = (110, 110)
        gravity = box2d.b2Vec2(0, 40)
        doSleep = True
        world = box2d.b2World(worldAABB, gravity, doSleep)
        #add some physics
        width = self.world_size[0]
        height = self.world_size[1]
        #for x, y, w, h in [(0, 0, width / 2, 1),
        #                   (0, 0, 1, height / 2),
        #                   (width - 2, 0, 1, height / 2),
        #                   (0, height - 2, width / 2, 1)]:
        for x, y, w, h in [(0, 0, 50, 1),
                           (0, 0, 1, 50),
                           (98, 0, 1, 50),
                           (0, 98, 50, 1)]:
            groundBodyDef = box2d.b2BodyDef()
            groundBodyDef.position = (x + w, y + h)
            groundBody = world.CreateBody(groundBodyDef)
            groundShapeDef = box2d.b2PolygonDef()
            groundShapeDef.SetAsBox(w, h)
            groundShapeDef.friction = 0.7
            groundShapeDef.restitution = 1
            groundBody.CreateShape(groundShapeDef)
            self.draw_AABB(surface, (x, y, w * 2, h * 2), BORDER_COLOR)
            print groundBody.position
        return world

#===============================================================================
# 
#    def load_constr(self, level=1):
#        '''Creating gamefield borders'''
#        if level == 1:
#            return ['x>10', 'x<990', 'y>10', 'y<990']
#        if level == 2:
#            return ['(x-500)**2+(y-500)**2<250000']
#        if level == 3:
#            return ['(x-500)**2+(y-500)**2<250000', '(x-500)**2+(y-500)**2>10000']
# 
#    def parse_constr(self, constraints):
#        '''Converting level constraints into a tree'''
#        parsed_constraints = []
#        for constr in constraints:
#            if constr.find('x') == -1 and constr.find('y') == -1:   #Inequality must have X and Y
#                raise(Exception("Constraint error, no parameter x and y: %s" % constr))
#            parsed_constraints.append(parser.expr(constr).compile())    #Parser adds compiled constr variable value to parsed_constraints list        
#        return parsed_constraints   #now its like a code
# 
#    def build_surface(self, constraints):
#        '''Creating game field'''
#        surface = pygame.Surface((1000, 1000))
#        surface.fill((125, 255, 125, 255))
# 
#        for x in range(0, 1000):
#            for y in range(0, 1000):
#                for constr in constraints:
#                    if not eval(constr):    #Execute compiled code
#                        surface.set_at((x, y), BORDER_COLOR) #Put pixel
# 
#        return pygame.transform.scale(surface, self.size).convert() #Resize field
#===============================================================================

    def draw_AABB(self, surface, (x, y, w, h), color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = [  self.transform((x, y)),
                    self.transform((x + w, y)),
                    self.transform((x + w, y + h)),
                    self.transform((x, y + h)),
                ]

        pygame.draw.aalines(surface, color, True, points)

    def transform(self, point):
        return point[0] * self.scale[0], point[1] * self.scale[1]

