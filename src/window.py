#!/usr/bin/env python

"""
Draws game window and handles events.
"""

__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "Date: 2011-04-22 17:34:04.129696 "

import sys
import os
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

if not pygame.font: LOGGER.warning('Fonts disabled')
if not pygame.mixer: LOGGER.warning('Sound disabled')

import physicsengine

#WORLD in meters
WIDTH = 100
HEIGHT = 100

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

        # initial window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

        screen_size = (800, 800)

        #gamefield size in meters for physics simulation
        real_size = (WIDTH, HEIGHT)
        self.window = pygame.display.set_mode(screen_size, pyg_loc.DOUBLEBUF)

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
        self.simulation = physicsengine.Simulation(screen_size, real_size)

        # init static bounding boxes
        self.simulation.create_level(0)

        # init dynamic balls
        for i in range(50):
            size = 0.5 + random.random() * 3
            pos = 10 + i / 50, 10 + i % 50
            ball = self.simulation.create_ball(pos, size)

            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            
            #ball.apply_force(x, y)
            ball.apply_force(1000, 1000)
        
            print dir(ball.physics)
            print dir(ball.groups())
            
        self.simulation.create_box((10, 10), (5, 5))

        self.allsprites = pygame.sprite.RenderUpdates(self.simulation.get_objects())

    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""

        LOGGER.debug('Game started')

        running = True
        # run until something tells us to stop
        while running:

            self.simulation.step()
            

            # tick pygame clock
            # you can limit the fps by passing the desired frames per second to tick()
            self.clock.tick(60)

            # update the title bar with our frames per second
            pygame.display.set_caption('Zonix %d fps' % self.clock.get_fps())

            #self.window.blit(self.bg_image, (0, 0))
            self.window.fill((134, 225, 0))
            self.allsprites.update()
            l = self.allsprites.draw(self.window)

            # render the screen, even though we don't have anything going on right now
            pygame.display.flip()

            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()

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
                if event.key == pyg_loc.K_UP:
                    self.simulation.applyGravity(0, 0)
                    #self.simulation.world.Refilter()
                if event.key == pyg_loc.K_DOWN:
                    self.simulation.applyGravity(0, 10)
                if event.key == pyg_loc.K_LEFT:
                    self.simulation.applyGravity(-10, 0)
                if event.key == pyg_loc.K_RIGHT:
                    self.simulation.applyGravity(10, 0)
                if event.key == pyg_loc.K_SPACE:
                    self.simulation.applyGravity(0, 0)
                # if the user presses escape, quit the event loop.
                if event.key == pyg_loc.K_ESCAPE:
                    return False
        return True

