#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import yaml
# noinspection PyCompatibility
# because we are installing it through pip
from typing import List
from random import shuffle, randint, randrange
from .errors import NoCards, OutOfCards, NotACard, CardNotFound
from .cards import CardType

log = logging.getLogger(__name__)


class Deck:
    """
    Deck you will be using. Make sure to create the instance somewhere reachable :)

    :param cards:       | Use this parameter if you don't plan to register your cards another way
                        | Cards can be either an instance of a  object, string or an integer,
                        | the documentation will be calling this :ref:`CardType` (because of Python's rank hinting)
    :rank cards:        List[:ref:`CardType`]
    :param reshuffle:   Set reshuffle to false if you want your deck not to reshuffle after it's depleted
    :rank reshuffle:    bool
    :param name:        Name of the deck, used when converting the Deck instance into string
    :rank name:         string
    """

    def __init__(self, cards: List[CardType] = None, reshuffle: bool = True, name: str = None):
        """
        Create the deck
        """

        self.name = name
        self._cards = cards
        if self._cards is None:
            self._cards = []
        self._discard_pile = []
        self._reshuffle = reshuffle
        self._save_location = None

    def draw(self) -> CardType:
        """
        Draw the topmost card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        if len(self._cards):
            card = self._cards.pop(0)
            self.reshuffle_if_empty()
            log.debug('Card drawn from top: %s', card)
            return card

        elif not self._reshuffle:
            log.debug('You tried to draw. No more cards to be drawn')
            raise OutOfCards('You tried to draw. No more cards to be drawn')

        else:
            log.debug('You tried to draw from an empty deck')
            raise NoCards('You tried to draw from an empty deck')

    def draw_bottom(self) -> CardType:
        """
        Draw the bottommost card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        if len(self._cards):
            card = self._cards.pop()
            self.reshuffle_if_empty()
            log.debug('Card drawn from bottom: %s', card)
            return card

        elif not self._reshuffle:
            log.debug('You tried to draw from bottom. No more cards to be drawn')
            raise OutOfCards('You tried to draw from bottom. No more cards to be drawn')

        else:
            log.debug('You tried to draw from bottom of an empty deck')
            raise NoCards('You tried to draw from bottom of an empty deck')

    def draw_random(self) -> CardType:
        """
        Draw a random card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        if len(self._cards):
            card = self._cards.pop(randrange(len(self._cards)))
            self.reshuffle_if_empty()
            log.debug('Card drawn randomly: %s', card)
            return card

        elif not self._reshuffle:
            log.debug('You tried to draw randomly. No more cards to be drawn')
            raise OutOfCards('You tried to draw randomly. No more cards to be drawn')

        else:
            log.debug('You tried to draw randomly from an empty deck')
            raise NoCards('You tried to draw randomly from an empty deck')

    # noinspection PyUnboundLocalVariable
    def draw_specific(self, specific_card: CardType) -> CardType:
        """
        Draw a specific card from the deck

        .. note::

            For card instances to match, they should have `__eq__`  method
            set to compare their equality. If you don't want to set those up,
            make sure their `__dict__` are the same and their name is the same.

            If you are using a string or an integer, don't worry about this!

        :param specific_card:   Card identical to the one you are looking for
        :rank specific_card:    :ref:`CardType`
        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        :raises CardNotFound:   when the card is not found in the deck
        """
        log.debug('Attempting to find card: %s', specific_card)
        if len(self._cards):
            found = False
            for available_card in self._cards:
                if card_compare(specific_card, available_card):
                    card = available_card
                    found = True
                    break
            if not found:
                log.debug('Specific card not found in the deck')
                raise CardNotFound('Specific card not found in the deck')
            self._cards.remove(card)
            self.reshuffle_if_empty()
            log.debug('Specific card drawn: %s', card)
            return card

        else:
            log.debug('You tried to draw a specific card from an empty deck')
            raise NoCards('You tried to draw a specific card from an empty deck')

    def card_exists(self, card: CardType) -> bool:
        """
        Checks if a card exists in the deck

        .. note::

            For card instances to match, they should have `__eq__`  method
            set to compare their equality. If you don't want to set those up,
            make sure their `__dict__` are the same and their name is the same.

            If you are using a string or an integer, don't worry about this!

        :param card:    Card identical to the one you are looking for
        :rank card:     :ref:`CardType`
        :return:        | True if exists
                        | False if doesn't exist
        :rtype:         bool
        """
        found = False
        for available_card in self._cards:
            if card_compare(card, available_card):
                found = True
                break
        log.debug('Card %s exists in the deck: %s', card, found)
        return found

    def shuffle(self):
        """
        Randomizes the order of cards in the deck

        :raises NoCards:     when there are no cards to be shuffled
        """
        if len(self._cards):
            shuffle(self._cards)
            log.debug('Deck shuffled')
        else:
            log.warning('You tried to shuffle an empty deck')
            raise NoCards('You tried to shuffle an empty deck')

    def reshuffle_if_empty(self):
        """
        Function that checks if the deck is out of cards and if reshuffle is true, it
        shuffles the discard pile back into the card pile
        """
        if not len(self._cards) and self._reshuffle:
            self.shuffle_back()

    def shuffle_back(self):
        """
        Shuffles the discard pile back into the main pile
        """
        for card in self._discard_pile:
            self._cards.append(card)
        self.shuffle()
        self._discard_pile = []
        log.debug('Cards have been shuffled back from the discard pile')

    def discard(self, card: CardType):
        """
        Puts a card into the discard pile

        :param card:        Card to be discarded
        :rank card:         :ref:`CardType`
        :raises NotACard:   When you try to insert False/None into a discard pile
        """
        log.debug("Card being discarded: %s", card)
        if card or type(card) == int:
            self._discard_pile.append(card)
            log.debug('Card %s discarded', card)
        # This had a reason, I remember testing something and ending
        # up with False/None in discard_pile - if anyone knows what
        # that was, let me know!
        else:
            log.warning('You tried to insert %s (rank(%s) into a discard pile',
                        card, type(card).__name__)
            raise NotACard('You tried to insert {} (rank({}) into a discard pile'
                           .format(card, type(card).__name__))

    def add_single(self, card: CardType):
        """
        Shuffles a single card into the active deck

        :param card:    Card you want to shuffle in
        :rank card:     :ref:`CardType`
        """
        self._cards.insert(randint(0, len(self._cards)), card)
        log.debug('New card shuffled into the deck')

    def add_many(self, cards: List[CardType]):
        """
        Shuffles a list of cards into the deck

        :param cards:   Cards you want to shuffle in
        :rank cards:    List[:ref:`CardType`]
        """
        for card in cards:
            self.add_single(card)
        log.debug('New cards shuffled into the deck')

    def show_top(self, number: int) -> List[CardType]:
        """
        Selects the top X cards from the deck without drawing them

        Useful for mechanics like scry in Magic The Gathering

        If there are less cards left than you want to show, it will show
        only the remaining cards

        :param number:      How many cards you want to show
        :rank number:       int
        :return:            Cards you want to show
        :rtype:             List[:ref:`CardType`]
        """
        return self._cards[0:number]

    def set_file_location(self, location):
        """
        used to update the location
        it will expand relative file path and ~ if it exists

        :param location: the location of the file
        """

        # I expanded the user and relative file paths so it's an absolute file path
        self._save_location = os.path.abspath(os.path.expanduser(location))

    def save(self, location=None):
        """
        saves the current deck into a yaml format so the deck can be retrieved at a later date

        useful if a game wishes to close and re open at a later date

        location is only needed once as it wil be saved
        if there is no location passed in the first time it will error

        :param location:    this specifies a file location to save to
        """
        if location:
            self.set_file_location(location)

        if self._save_location is None:
            raise Exception("No file location defined")

        # setting the save location to None before saving
        # this is so the file path is not save in the file
        # only reason is so the original file path is never saved for security reasons
        location = self._save_location
        self._save_location = None

        with open(location, 'w') as yaml_file:
            yaml.dump(self, yaml_file)

        # re applying the save location
        self._save_location = location

    def load(self, location=None):
        """
        loads a deck into the deck
        first time a location must be passed
        this location value can then be used by both save and load
        to overwrite simply pass in a new value

        :param location:    this specifies the file location to load from
        """
        if location:
            self.set_file_location(location)

        if self._save_location is None:
            raise Exception("No file location defined")

        # I del save_location so self.save_location does not get overwritten
        data = yaml.load(open(self._save_location)).__dict__
        del data["_save_location"]
        self.__dict__.update(data)

    def load_standard_deck(self):
        """
        Loads a standard deck of 52 cards into the deck
        """
        location = os.path.join(os.path.dirname(__file__), "standard_deck.yml")

        # removing save location so it is not overwritten
        data = yaml.load(open(location)).__dict__
        del data["_save_location"]
        self.__dict__.update(data)

    @property
    def cards_left(self) -> int:
        """
        Cards left in the deck

        :return:    Number of cards in the deck
        :rtype:     int
        """
        if len(self._cards):
            return len(self._cards)
        else:
            return 0

    @property
    def discarded(self) -> int:
        """
        Cards in the discard pile

        :return:    Number of cards in the discard pile
        :rtype:     int
        """
        return len(self._discard_pile)

    @property
    def empty(self) -> bool:
        """


        :return:    Whether the deck is empty
        :rtype:     bool
        """
        if len(self._cards):
            return False
        else:
            return True

    @property
    def file_location(self) -> str:
        """
        returns the file location of which current is loaded from/ will be saved to

        :return:    file location
        :rtype:     str
        """
        return self._save_location

    def __repr__(self) -> str:
        """
        Used for representation of the object

        called with repr(Deck)

        :return:    'Deck of cards'
        :rtype:     string
        """
        return 'Deck(cards={0}, discarded={3}, reshuffle={1}, name={2})' \
            .format(self.cards_left, self._reshuffle, self.name, self.discarded)

    def __str__(self) -> str:
        """
        Used for representation of the object for humans

        called with str(Deck)

        This method is also called when you are providing arguments to str.format(), you can just provide
        your Deck instance and it will magically know the name, yay!

        :return:    Name of the deck if it has a name  or 'Deck of cards' if it has none
        :rtype:     string
        """

        if self.name:
            return self.name
        else:
            return 'Deck of cards'

    def __len__(self) -> int:
        """
        Instead of doing len(Deck.cards) you can just check len(Deck)

        It's however recommended to use the :py:attr:`cards_left` attribute

        :return:    Number of cards left in the deck
        :rtype:     int
        """
        return len(self._cards)


def card_compare(card: CardType, second_card: CardType) -> bool:
    """
    Function for comparing two cards. First it checks their `__eq__`,
    if that returns False, it checks `__dict__` and name of the Class
    that spawned them .

    :param card:                First card to match
    :rank card:                 :ref:`CardType`
    :param second_card:         Second card to match
    :rank second_card:          :ref:`CardType`
    :return:                    Whether they are the same
    :rtype:                     bool
    """
    identity = False
    if second_card == card:
        identity = True
    else:
        # For comparing instances of objects that have different IDs and don't
        # have their __eq__ method set up to work when comparing.
        try:
            if second_card.__dict__ == card.__dict__ \
                    and type(second_card).__name__ == type(card).__name__:
                identity = True
        except AttributeError:
            pass
    return identity
