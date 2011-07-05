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

BORDER_COLOR = pygame.Color(0, 0, 255, 255)

class GameField(pygame.sprite.Sprite):
    '''Represents a game field as a set of inequalities.'''

    def __init__(self, level=3, size=(600, 600)):
        pygame.sprite.Sprite.__init__(self)
        self.constraints = self.parse_constr(self.load_constr(level))
        self.size = size
        self.image = self.build_surface(self.constraints)
        self.rect = self.image.get_rect()   # Rect area for updating image

    
    def load_constr(self, level=1):
        '''Creating gamefield borders'''        
        if level == 1:
            return ['x>10', 'x<990', 'y>10', 'y<990']
        if level == 2:
            return ['(x-500)**2+(y-500)**2<250000']
        if level == 3:
            return ['(x-500)**2+(y-500)**2<250000', '(x-500)**2+(y-500)**2>10000']

    def parse_constr(self, constraints):
        '''Converting level constraints into a tree'''
        parsed_constraints = []
        for constr in constraints:
            if constr.find('x') == -1 and constr.find('y') == -1:   #Inequality must have X and Y
                raise(Exception("Constraint error, no parameter x and y: %s" % constr))
            parsed_constraints.append(parser.expr(constr).compile())    #Parser adds compiled constr variable value to parsed_constraints list        
        return parsed_constraints   #now its like a code

    def build_surface(self, constraints):
        '''Creating game field'''
        surface = pygame.Surface((1000, 1000))
        surface.fill((125, 255, 125, 255))
    
        for x in range(0, 1000):
            for y in range(0, 1000):
                for constr in constraints:
                    if not eval(constr):    #Execute compiled code
                        surface.set_at((x, y), BORDER_COLOR) #Put pixel

        return pygame.transform.scale(surface, self.size).convert() #Resize field
    

