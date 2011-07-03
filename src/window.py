#!/usr/bin/env python

"""
Draws game window and handles events.
"""

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "Date: 2011-04-22 17:34:04.129696 "

import sys
import logging
import colorer
LOGGER = logging.getLogger('main.window')

try:
    import pygame
    import pygame.locals as pyg_loc
except ImportError as ex:
    #LOGGER.exception("%s Failed to load module." % __file__)
    sys.exit("%s Failed to load module. %s" % (__file__, ex))

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

        # create background
        self.background = pygame.Surface(self.window.get_size()).convert()
        self.background.fill((250, 250, 250))

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
        self.gamefield = gamefield.GameField()

        # init 1 ball
        self.ball = gameobjects.Ball()

        self.allsprites = pygame.sprite.RenderPlain([self.ball])

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


            self.window.blit(self.background, (0, 0))
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
