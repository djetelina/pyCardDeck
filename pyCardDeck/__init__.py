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
__version__ = '1.0.0.dev1'

from .deck import *
from .errors import *
from .cards import *
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
