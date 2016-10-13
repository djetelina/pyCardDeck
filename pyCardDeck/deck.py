#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import yaml
import jsonpickle
# noinspection PyCompatibility
# because we are installing it through pip
from typing import List
from random import shuffle, randint, randrange
from .errors import OutOfCards, NotACard, NoCards, CardNotFound, UnknownFormat
from .cards import CardType

log = logging.getLogger(__name__)


class Deck:
    """
    Deck you will be using. Make sure to create the instance somewhere reachable :)

    :param cards:       | Use this parameter if you don't plan to register your cards another way
                        | Cards can be either an instance of a  object, string or an integer,
                        | the documentation will be calling this :ref:`CardType` (because of Python's rank hinting)
    :type cards:        List[:ref:`CardType`]
    :param reshuffle:   Set reshuffle to false if you want your deck not to reshuffle after it's depleted
    :type reshuffle:    bool
    :param name:        Name of the deck, used when converting the Deck instance into string
    :type name:         string
    """

    def __init__(self, cards: object = None, reshuffle: object = True, name: object = None):
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

    def _get_card(self, position: str = "top") -> CardType:
        """
        Helper function for drawing from the deck. Shouldn't be used

        :param position:        Where to draw from
        :type position:         str
        :return:                Drawn card
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        if len(self._cards):
            positions = {
                "top": 0,
                "bottom": len(self._cards) - 1,
                "random": randrange(len(self._cards))
            }
            card = self._cards.pop(positions[position])
            self.reshuffle_if_empty()
            log.debug('Card drawn from %s: %s', (position, card))
            return card

        elif not self._reshuffle:
            log.debug('You tried to draw. No more cards to be drawn. Position: %s', position)
            raise OutOfCards('You tried to draw. No more cards to be drawn. Position: %s', position)

        else:
            log.debug('You tried to draw from an empty deck. Position: %s', position)
            raise NoCards('You tried to draw from an empty deck. Position: %s', position)

    def draw(self) -> CardType:
        """
        Draw the topmost card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("top")

    def draw_bottom(self) -> CardType:
        """
        Draw the bottommost card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("bottom")

    def draw_random(self) -> CardType:
        """
        Draw a random card from the deck

        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("random")

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
        :type specific_card:    :ref:`CardType`
        :return:                Card from the list
        :rtype:                 :ref:`CardType`
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        :raises CardNotFound:   when the card is not found in the deck
        """
        log.debug('Attempting to find card: %s', specific_card)
        if len(self._cards):
            for available_card in self._cards:
                if _card_compare(specific_card, available_card):
                    card = available_card
                    break
            else:
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
        :type card:     :ref:`CardType`
        :return:        | True if exists
                        | False if doesn't exist
        :rtype:         bool
        """
        found = False
        for available_card in self._cards:
            if _card_compare(card, available_card):
                found = True
                break
        log.debug('Card %s exists in the deck: %s', card, found)
        return found

    def shuffle(self) -> None:
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

    def reshuffle_if_empty(self) -> None:
        """
        Function that checks if the deck is out of cards and if reshuffle is true, it
        shuffles the discard pile back into the card pile
        """
        if not len(self._cards) and self._reshuffle:
            self.shuffle_back()

    def shuffle_back(self) -> object:
        """
        Shuffles the discard pile back into the main pile
        """
        for card in self._discard_pile:
            self._cards.append(card)
        self.shuffle()
        self._discard_pile = []
        log.debug('Cards have been shuffled back from the discard pile')

    def discard(self, card: CardType) -> None:
        """
        Puts a card into the discard pile

        :param card:        Card to be discarded
        :type card:         :ref:`CardType`
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

    def add_single(self, card: CardType, position: int = False) -> None:
        """
        Shuffles (or inserts) a single card into the active deck

        :param card:        Card you want to insert
        :type card:         :ref:`CardType`
        :param position:    | If you want to let player insert card to a specific location, use position
                            | where 0 = top of the deck, 1 = second card from top etc.
                            | By default the position is random
        :type position:     int
        """
        if position is not False:
            self._cards.insert(position, card)
            log.debug("Card %s inserted to position %i", card, position)
            log.debug(self._cards)
        else:
            self._cards.insert(randint(0, len(self._cards)), card)
            log.debug('Card %s shuffled into the deck', card)

    def add_many(self, cards: List[CardType]) -> None:
        """
        Shuffles a list of cards into the deck

        :param cards:   Cards you want to shuffle in
        :type cards:    List[:ref:`CardType`]
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
        :type number:       int
        :return:            Cards you want to show
        :rtype:             List[:ref:`CardType`]
        """
        return self._cards[0:number]

    def set_file_location(self, location) -> None:
        """
        Used to update the location
        It will expand relative file path and ~ if it exists
        The file path should be relative to the main script
        A filename must be passed in as part of location

        Example: ~/mydeck.yml

        :param location: the location of the file
        """

        # I expanded the user and relative file paths so it's an absolute file path
        self._save_location = os.path.abspath(os.path.expanduser(location))

    def export(self, fmt: str, to_file: bool = False, location: str = None) -> str:
        """
        Export the deck. By default it returns string with either JSON or YaML,
        but if you set `to_file=True`, you can instead save the deck as a file.
        If no location (with filename) is provided, it'll save to the folder the script
        is opened from as `exported_deck` without an extension.

        :param fmt:             Desired format, either YaML or JSON
        :type fmt:              str
        :param to_file:         Whether you want to get a string back or save to a file
        :type to_file:          bool
        :param location:        Where you want to save your file - include file name!
        :type location:         str
        :raises UnknownFormat:  When entered format is not supported
        :return:                Your exported deck as a string in your desired format
        :rtype:                 str
        """

        # Eliminate some human error
        format_stripped = fmt.lower().strip()

        # Find out where we want to export, if we do
        if location:
            self.set_file_location(location)
        # if we don't know where, let's make a default export file
        elif self._save_location is None:
            self.set_file_location("exported_deck")

        # Hide location for security from exported deck
        temp_location = self._save_location
        self._save_location = None

        # Get the actual exported data
        exported = _get_exported_string(format_stripped, self)

        # Restore saved value
        self._save_location = temp_location

        if to_file:
            with open(self._save_location, 'w') as target_file:
                target_file.writelines(exported)
            log.debug("File exported to: %s", self._save_location)

        # We return the string either way, because why not?
        return exported

    def load(self, to_load: str, is_file: bool = False) -> None:
        """
        Way to override a deck instance with a saved deck from either yaml, JSON
        or a file with either of those.

        The library will first try to check if you have a save location saved, then verifies
        if the file exists as a path to a file. If it doesn't, it'l assume it's a string with one of
        the supported formats and will load from those.

        :param to_load:         | This should be either a path to a file or a string containing
                                | json/yaml generated by Deck.export(). It's not safe to trust your users
                                | with this, as they can provide harmful pickled JSON (see jsonpickle docs for more)
        :type to_load:          str
        :param is_file:         whether to_load is a file path or actual data. Default is False
        :type is_file:          bool
        :raises UnknownFormat:  When the entered yaml or json is not valid
        """
        # I tried auto identifying but it didn't work, everything could be a file so it would always accept it
        if is_file:
            self.set_file_location(to_load)
            with open(self._save_location, 'r') as file:
                loadable = file.read()
        else:
            loadable = to_load
        # This is not really an elegant solution, but it works
        # noinspection PyBroadException
        try:
            result = jsonpickle.decode(loadable)
            log.debug("loading JSON")
        # When we try to catch a specific exception (JSONDecodeError), it doesn't exist in 3.3 and 3.4
        except Exception as _:
            result = yaml.load(loadable)
            log.debug("loading YAML")
        try:
            del result.__dict__["_save_location"]
            self.__dict__.update(result.__dict__)
        except AttributeError:
            raise UnknownFormat

    def load_standard_deck(self) -> None:
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
    def json(self) -> str:
        """
        Alternative to Deck.export("json")

        :return:    jsonpickled Deck
        :rtype:     str
        """
        return self.export("json", to_file=False)

    @property
    def yaml(self) -> str:
        """
        Alternative to Deck.export("yaml")

        :return:    yaml dump of the Deck
        :rtype:     str
        """
        return self.export("yaml")

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
        Returns the file location of which current is loaded from/ will be saved to

        :return:    file location
        :rtype:     str
        """
        return self._save_location

    def __repr__(self) -> str:  # pragma: no cover
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

    def __getitem__(self, position):
        """
        For more pythonic usage

        Allows for slicing and other things like random.choice(Deck)
        """
        return self._cards[position]

    def __setitem__(self, position, card):
        """
        For more pythonic usage

        Allows for things like random.shuffle(Deck)
        """
        self._cards[position] = card


def _card_compare(card: CardType, second_card: CardType) -> bool:
    """
    Function for comparing two cards. First it checks their `__eq__`,
    if that returns False, it checks `__dict__` and name of the Class
    that spawned them .

    :param card:                First card to match
    :type card:                 :ref:`CardType`
    :param second_card:         Second card to match
    :type second_card:          :ref:`CardType`
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


def _get_exported_string(format_stripped: str, deck: Deck) -> str:
    """
    Helper function to Deck.export()

    :param format_stripped:     Desired format stripped of any spaces and lowercase
    :type format_stripped:      str
    :param deck:                instance of a Deck
    :type deck:                 :ref:`Deck`
    :return:                    YAML/JSON string of the deck
    :rtype:                     str
    :raises UnknownFormat:      when it doesn't recognize format_stripped
    """
    if format_stripped == "yaml" or format_stripped == "yml":
        exported = yaml.dump(deck)
        log.debug("Exported deck %r to a yaml string", deck)
    elif format_stripped == "json":
        exported = jsonpickle.encode(deck)
        log.debug("Exported deck %r to a json string", deck)
    else:
        log.debug("Unknown format: %s", format)
        raise UnknownFormat("Unknown format: {}".format(format))
    return exported
