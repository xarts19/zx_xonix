#!/usr/bin/env python
'''
Handles game resources.
'''
__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "Jul 3, 2011"

import os
import sys
import logging
import colorer
LOGGER = logging.getLogger('main.data')

import pygame
import pygame.locals as pyg_loc

IMG_DIR = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..', 'data', 'img'))

def load_image(name, colorkey=None):
    '''Load image. Uses red box as fallback.'''
    fullname = os.path.join(IMG_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        LOGGER.exception("Can't load image: %s", message)
        image = pygame.Surface((50, 50))
        image.fill((255, 0, 0, 255))
        colorkey = None
    image = image.convert()
    if colorkey is not None:
        if colorkey is (-1):
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pyg_loc.RLEACCEL)
    return image


LEVELS = {0: [((0, 0), (100, 2)),
              ((0, 0), (2, 100)),
              ((98, 0), (2, 100)),
              ((0, 98), (100, 2)),
             ],
          }

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
