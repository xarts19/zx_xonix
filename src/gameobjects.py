#!/usr/bin/env python
'''
Module includes various game objects.
'''

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "June 30, 2011"

import pygame

import logging
import colorer
LOGGER = logging.getLogger('main.gameobjects')

class GameObject(pygame.sprite.Sprite):
    '''Class, representing base game object. Subject of derivation of other,
    more specific game objects.
    '''

    def __init__(self):
        pass
