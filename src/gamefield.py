#!/usr/bin/env python
'''
Module will include GameField class and various utility functions for working with it.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame

import parser
import logging
import colorer
LOGGER = logging.getLogger('main.gamefield')

PIXEL_COLOR = pygame.Color(0, 0, 255, 255)

class GameField(pygame.sprite.Sprite):
    '''Represents a game field as a set of inequalities.'''

    def __init__(self, level=1, size=(600, 600)):
        pygame.sprite.Sprite.__init__(self)
        self.constraints = self.parse_constr(self.load_constr(level))
        self.size = size
        self.image = self.build_surface(self.constraints)
        self.rect = self.image.get_rect()

    def load_constr(self, level=1):
        if level == 1:
            return ['x>10', 'x<990', 'y>10', 'y<990']
        if level == 2:
            return ['(x-500)**2+(y-500)**2<250000']

    def parse_constr(self, constraints):
        parsed_constraints = []
        for constr in constraints:
            if constr.find('x') == -1 and constr.find('y') == -1:
                raise(Exception("Constraint error, no parameter x and y: %s" % constr))
            parsed_constraints.append(parser.expr(constr).compile())
        return parsed_constraints

    def build_surface(self, constraints):
        surface = pygame.Surface((1000, 1000))
        surface.fill((125, 255, 125, 255))

        for constr in constraints:
            for x in range(0, 1000):
                for y in range(0, 1000):
                    if not eval(constr):
                        surface.set_at((x, y), PIXEL_COLOR)

        return pygame.transform.scale(surface, self.size).convert()

