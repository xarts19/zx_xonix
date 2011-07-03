#!/usr/bin/env python
'''
Main module
'''
__author__ = "Xarts19 (xarts19@gmail.com)"
__version__ = "Version: 0.0.1 "
__date__ = "Jul 3, 2011"

import optparse
import logging
import colorer
LOGGER = logging.getLogger('main')

LOGGER_FORMAT = "%(name)s--%(levelname)s--%(asctime)s - %(message)s"
LOGGER_DATE_FORMAT = "%d-%m-%y %H:%M:%S"

import window

def init_logging(debug_level):
    '''Initialize logging system.'''
    LOGGER.setLevel(debug_level)
    LOGGER.propagate = 0
    streamLogger = logging.StreamHandler()
    streamLogger.setLevel(debug_level)
    formatter = logging.Formatter(LOGGER_FORMAT, LOGGER_DATE_FORMAT)
    streamLogger.setFormatter(formatter)
    LOGGER.addHandler(streamLogger)


def parse_args():
    '''Parse cli arguments.'''
    parser = optparse.OptionParser(description=__doc__, prog='Existence',
                        version=__version__)
    parser.add_option('-d', '--debug', action='store_const', dest='debug',
                        const=logging.DEBUG, help='show debug information')
    parser.add_option('-v', '--verbose', action='store_const', dest='debug',
                        const=logging.INFO, help='show additional information')
    opts = parser.parse_args()[0]

    debug_level = logging.WARNING
    if opts.debug:
        debug_level = opts.debug
    init_logging(debug_level)

    LOGGER.debug('cli options: %s', opts)


def main():
    '''Launch the program.'''
    parse_args()
    game = window.Game()
    game.run()


if __name__ == "__main__":
    main()
