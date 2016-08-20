#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from random import shuffle, choice, randint
from .errors import NoCards, OutOfCards, NotACard, CardNotFound

log = logging.getLogger(__name__)


class Deck:
    """
    Deck you will be using. Make sure to create the instance somewhere reachable :)

    :param cards:       | Use this parameter if you don't plan to register your cards another way
                        | Cards can be anything except False/None, it's however recommended to
                        use (TBD) base class Card
    :type cards:        list
    :param reshuffle:   Set reshuffle to false if you want your deck not to reshuffle after it's depleted
    :type reshuffle:    bool
    :param name:        Name of the deck, used when converting the Deck instance into st ring
    :type name:         string
    """

    def __init__(self, cards=None, reshuffle=True, name=None):
        """
        Create the deck
        """

        self.name = name
        self._cards = cards
        if self._cards is None:
            self._cards = []
        self._discard_pile = []
        self.reshuffle = reshuffle

    def draw(self):
        """
        Draw the topmost card from the deck

        :return:              Card from the list
        :raises OutOfCards:    when there are no cards in the deck
        :raises NoCards:       when the deck runs out of cards (no reshuffle)
        """
        if self._cards:
            card = self._cards.pop(0)
            if len(self._cards) == 0:
                if self.reshuffle:
                    self.shuffle_back()
            log.debug('Card drawn from top: {0}'.format(card))
            return card

        elif not self.reshuffle:
            log.debug('You tried to draw. No more cards to be drawn')
            raise OutOfCards('You tried to draw. No more cards to be drawn')

        else:
            log.debug('You tried to draw from an empty deck')
            raise NoCards('You tried to draw from an empty deck')

    def draw_bottom(self):
        """
        Draw the bottommost card from the deck

        :return:              Card from the list
        :raises OutOfCards:    when there are no cards in the deck
        :raises NoCards:       when the deck runs out of cards (no reshuffle)
        """
        if self._cards:
            card = self._cards.pop()
            if len(self._cards) == 0:
                if self.reshuffle:
                    self.shuffle_back()
            log.debug('Card drawn from bottom: {0}'.format(card))
            return card

        elif not self.reshuffle:
            log.debug('You tried to draw from bottom. No more cards to be drawn')
            raise OutOfCards('You tried to draw from bottom. No more cards to be drawn')

        else:
            log.debug('You tried to draw from bottom of an empty deck')
            raise NoCards('You tried to draw from bottom of an empty deck')

    def draw_random(self):
        """
        Draw a random card from the deck

        :return:              Card from the list
        :raises OutOfCards:    when there are no cards in the deck
        :raises NoCards:       when the deck runs out of cards (no reshuffle)
        """
        if self._cards:
            card = choice(self._cards)
            self._cards.remove(card)
            if len(self._cards) == 0:
                if self.reshuffle:
                    self.shuffle_back()
            log.debug('Card drawn randomly: {0}'.format(card))
            return card

        elif not self.reshuffle:
            log.debug('You tried to draw randomly. No more cards to be drawn')
            raise OutOfCards('You tried to draw randomly. No more cards to be drawn')

        else:
            log.debug('You tried to draw randomly from an empty deck')
            raise NoCards('You tried to draw randomly from an empty deck')

    # noinspection PyUnboundLocalVariable
    def draw_specific(self, specific_card: object) -> object:
        """
        Draw a specific card from the deck

        .. note::

            For card instances to match, the return of their __dict__ methods must
            equal. If you are not using objects, exact equality will go through just
            fine (`'a' == 'a'`).

        :param specific_card:   Card identical to the one you are looking for
        :type specific_card:    object
        :return:                Card from the list
        :rtype:                 object
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        :raises CardNotFound:   when the card is not found in the deck
        """
        log.debug('Attempting to find card: {}'.format(specific_card))
        if self._cards:
            found = False
            for available_card in self._cards:
                if self.card_compare(specific_card, available_card):
                    card = available_card
                    found = True
                    break
            if not found:
                log.debug('Specific card not found in the deck')
                raise CardNotFound('Specific card not found in the deck')
            self._cards.remove(card)
            if len(self._cards) == 0:
                if self.reshuffle:
                    self.shuffle_back()
            log.debug('Specific card drawn: {0}'.format(card))
            return card

        else:
            log.debug('You tried to draw a specific card from an empty deck')
            raise NoCards('You tried to draw a specific card from an empty deck')

    def card_exists(self, card: object) -> bool:
        """
        Checks if a card exists in the deck

        .. note::

            For card instances to match, the return of their __dict__ methods must
            equal. If you are not using objects, exact equality will go through just
            fine (`'a' == 'a'`).

        :param card:    Card identical to the one you are looking for
        :type card:     object
        :return:        | True if exists
                        | False if doesn't exist
        :rtype:         bool
        """
        found = False
        for available_card in self._cards:
            if self.card_compare(card, available_card):
                found = True
                break
        log.debug('Card {0} exists in the deck: {1}'.format(card, found))
        return found

    @staticmethod
    def card_compare(card: object, available_card: object) -> bool:
        identity = False
        try:
            if available_card.__dict__ == card.__dict__:
                identity = True
        except AttributeError:
            if available_card == card:
                identity = True
        return identity

    def shuffle(self):
        """
        Randomizes the order of cards in the deck

        :raises NoCards:     when there are no cards to be shuffled
        """
        if self._cards:
            shuffle(self._cards)
            log.debug('Deck shuffled')
        else:
            log.warning('You tried to shuffle an empty deck')
            raise NoCards('You tried to shuffle an empty deck')

    def shuffle_back(self):
        """
        Shuffles the discard pile back into the main pile
        """
        for card in self._discard_pile:
            self._cards.append(card)
        self.shuffle()
        self._discard_pile = []
        log.debug('Cards have been shuffled back from the discard pile')

    def discard(self, card: object):
        """
        Puts a card into the discard pile

        :param card:        Card to be discarded
        :type card:         object
        :raises NotACard:   When you try to insert False/None into a discard pile
        """
        log.debug("Card being discarded: {}".format(card))
        if card or type(card) == int:
            self._discard_pile.append(card)
            log.debug('Card {0} discarded'.format(card))
        # This had a reason, I remember testing something and ending
        # up with False/None in discard_pile - if anyone knows what
        # that was, let me know!
        else:
            log.warning('You tried to insert {} (type({}) into a discard pile'
                        .format(card, type(card).__name__))
            raise NotACard('You tried to insert {} (type({}) into a discard pile'
                           .format(card, type(card).__name__))

    def add_single(self, card: object):
        """
        Shuffles a single card into the active deck

        :param card:    Card you want to shuffle in
        :type card:     object
        """
        self._cards.insert(randint(0, len(self._cards)), card)
        log.debug('New card shuffled into the deck')

    def add_many(self, cards: list):
        """
        Shuffles a list of cards into the deck

        :param cards:   Cards you want to shuffle in
        :type cards:    list
        """
        for card in cards:
            self.add_single(card)
        log.debug('New cards shuffled into the deck')

    def show_top(self, number: int) -> list:
        """
        Selects the top X cards from the deck without drawing them

        Useful for mechanics like scry in Magic The Gathering

        If there are less cards left than you want to show, it will show
        only the remaining cards

        :param number:      How many cards you want to show
        :type number:       int
        :return:            Cards you want to show
        :rtype:             list
        """
        return self._cards[0:number]

    @property
    def cards_left(self) -> int:
        """
        Cards left in the deck

        :return:    Number of cards in the deck
        :rtype:     int
        """
        if self._cards:
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
        if self._cards:
            return False
        else:
            return True

    def __repr__(self) -> str:
        """
        Used for representation of the object

        called with repr(Deck)

        :return:    'Deck of cards'
        :rtype:     string
        """
        return 'Deck instance: cards={0}, discarded={3}, reshuffle={1}, name={2}'\
            .format(self.cards_left, self.reshuffle, self.name, self.discarded)

    def __str__(self) -> str:
        """
        Used for representation of the object for humans

        called with str(Deck)

        This method is also called when you are providing arguments to str.format(), you can just provide
        your Deck instance and it will magically know the name, yay!

        :return:    | Name of the deck if it has a name
                    | or 'Deck of cards' if it has none
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
