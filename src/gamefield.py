#!/usr/bin/env python
'''
Module will include GameField class and various utility functions for working with it.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame

import logging
import colorer
LOGGER = logging.getLogger('main.gamefield')

class GameField(pygame.sprite.Sprite):
    '''Represents a game field as a set of inequalities.'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

