#!/usr/bin/env python

"""
Draws game window and handles events.
"""

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "Date: 2011-04-22 17:34:04.129696 "

import sys
import random
import logging
import colorer
LOGGER = logging.getLogger('main.window')

try:
    import pygame
    import pygame.locals as pyg_loc
except ImportError as ex:
    #LOGGER.exception("%s Failed to load module." % __file__)
    sys.exit("%s Failed to load module. %s" % (__file__, ex))

import Box2D as box2d

if not pygame.font: LOGGER.warning('Fonts disabled')
if not pygame.mixer: LOGGER.warning('Sound disabled')

import gamefield
import gameobjects
import physicsengine
import data

class Game(object):
    """Our game object! This is a fairly simple object that handles the
    initialization of pygame and sets up our game to run."""

    def __init__(self):
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools."""

        LOGGER.debug('Initializing window')

        # load and set up pygame
        pygame.init()

        # create our window
        self.window = pygame.display.set_mode((600, 600))

        # clock for ticking
        self.clock = pygame.time.Clock()

        # set the window title
        pygame.display.set_caption("Zonix")

        # disable mouse
        pygame.mouse.set_visible(0)

        # tell pygame to only pay attention to certain events
        # we want to know if the user hits the X on the window, and we
        # want keys so we can close the window with the esc key
        pygame.event.set_allowed([pyg_loc.QUIT, pyg_loc.KEYDOWN])

        # init game field
        #self.gamefield = gamefield.GameField(size=self.window.get_size())
        # create world
        worldAABB = box2d.b2AABB()
        worldAABB.lowerBound = (-100, -100)
        worldAABB.upperBound = (700, 700)
        gravity = (0, 0)
        doSleep = True
        world = box2d.b2World(worldAABB, gravity, doSleep)
        #add some physics
        for x, y, w, h in [(0, 0, 300, 10), (0, 0, 10, 300), (580, 0, 300, 10), (0, 580, 10, 300)]:
            groundBodyDef = box2d.b2BodyDef()
            groundBodyDef.position = (x, y)
            groundBody = world.CreateBody(groundBodyDef)
            groundShapeDef = box2d.b2PolygonDef()
            groundShapeDef.SetAsBox(w / 2, h / 2)
            groundBody.CreateShape(groundShapeDef)

        # init 5 balls
        self.balls = []
        for i in range(5):
            size = random.randint(30, 50)
            pos = random.randint(50, self.window.get_size()[0] - 50), \
                    random.randint(50, self.window.get_size()[1] - 50)
            self.balls.append(gameobjects.Ball(size, pos))
            speed = random.randint(50, 200), random.randint(50, 200)
            self.balls[-1].update_speed(speed)

            #add some physics
            bodyDef = box2d.b2BodyDef()
            bodyDef.position = pos
            body = world.CreateBody(bodyDef)
            shapeDef = box2d.b2PolygonDef()
            shapeDef.SetAsBox(size / 2, size / 2)
            shapeDef.density = 1
            shapeDef.friction = 0.3
            body.CreateShape(shapeDef)

        self.allsprites = pygame.sprite.RenderPlain(self.balls)

    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        LOGGER.debug('Game started')

        running = True
        # run until something tells us to stop
        while running:

            # tick pygame clock
            # you can limit the fps by passing the desired frames per seccond to tick()
            self.clock.tick(60)

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()

            # update the title bar with our frames per second
            pygame.display.set_caption('Zonix %d fps' % self.clock.get_fps())

            self.window.blit(self.gamefield.image, (0, 0))
            self.allsprites.update()
            self.allsprites.draw(self.window)

            # render the screen, even though we don't have anything going on right now
            pygame.display.flip()

        LOGGER.debug('Game finished')

    def handleEvents(self):
        """Poll for PyGame events and behave accordingly. Return false to stop
        the event loop and end the game."""

        # poll for pygame events
        for event in pygame.event.get():
            if event.type == pyg_loc.QUIT:
                return False

            # handle user input
            elif event.type == pyg_loc.KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == pyg_loc.K_ESCAPE:
                    return False
        return True

