# -*- coding: utf-8 -*-

"""
pyCardDeck
==========

Deck of cards with all the logic, so you don't have to!

:copyright:     (c) 2016 David Jetelina
:license:       MIT
"""

__title__ = 'pyCardDeck'
__author__ = 'David Jetelina'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 David Jetelina'
__version__ = '1.3.3'

from .deck import *
from .errors import *
from .cards import *
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
