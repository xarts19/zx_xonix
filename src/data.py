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
    return image, image.get_rect()
