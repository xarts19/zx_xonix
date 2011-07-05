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

import data

class GameObject(pygame.sprite.Sprite):
    '''Class, representing base game object. Subject of derivation of other,
    more specific game objects.'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



class Ball(GameObject):
    '''Round object.'''

    def __init__(self, size=40, pos=(50, 50)):
        GameObject.__init__(self)
        self.size = size
        self.position = pos
        self.image, self.rect = data.load_image('ball.gif', -1)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.position
        self.rect.center = pygame.mouse.get_pos()

