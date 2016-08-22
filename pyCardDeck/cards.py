#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# noinspection PyCompatibility
# because we are installing it through pip
from typing import Union


class BaseCard:
    """
    This is an example Card, showing that each Card should have a name.

    This is good, because when we can show player their cards just by converting
    them to strings.
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '{0}({1.__dict__})'.format(type(self).__name__, self)


class PokerCard(BaseCard):
    """
    Example Poker Card, since Poker is a a deck of Unique cards,
    we can say that if their name equals, they equal too.
    """

    def __init__(self, suit: str, rank: str, name: str):
        # Define self.name through BaseCard Class
        super().__init__("{} of {}".format(name, suit))
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        return self.name == other


CardType = Union[BaseCard, PokerCard, object, str, int]
