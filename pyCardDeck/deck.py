import logging
import os
from collections.abc import Iterator
from random import shuffle, randint, randrange

import jsonpickle
import yaml

from .cards import CardType
from .errors import OutOfCards, NotACard, NoCards, CardNotFound, UnknownFormat

log = logging.getLogger(__name__)


class Deck:
    """
    Deck you will be using. Make sure to create the instance somewhere reachable :)

    :param cards:       Use this parameter if you don't plan to register your cards another way.
                        Cards can be either an instance of an object, string or an integer.
    :param reshuffle:   Set reshuffle to false if you want your deck not to reshuffle after it's depleted
    :param name:        Name of the deck, used when converting the Deck instance into string
    :param discard:     optional Deck object to use as discard pile
    """

    def __init__(
        self,
        cards: list[CardType] | None = None,
        reshuffle: bool = True,
        name: str | None = None,
        discard: "Deck | None" = None,
    ):
        """
        Create the deck
        """

        self.name = name
        if cards is None:
            self._cards: list[CardType] = []
        else:
            self._cards = cards
        if discard is None:
            self._discard_pile: Deck | list[CardType] = []
        else:
            self._discard_pile = discard
        self._reshuffle = reshuffle
        self.set_file_location("exported_deck")

    def _get_card(self, position: str = "top") -> CardType:
        """
        Helper function for drawing from the deck. Shouldn't be used

        :param position:        Where to draw from
        :return:                Drawn card
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        if self._cards:
            positions = {
                "top": 0,
                "bottom": len(self._cards) - 1,
                "random": randrange(len(self._cards)),
            }
            card = self._cards.pop(positions[position])
            self.reshuffle_if_empty()
            log.debug("Card drawn from %s: %s", position, card)
            return card

        elif not self._reshuffle:
            log.debug(
                "You tried to draw. No more cards to be drawn. Position: %s", position
            )
            raise OutOfCards(
                "You tried to draw. No more cards to be drawn. Position: %s", position
            )

        else:
            log.debug("You tried to draw from an empty deck. Position: %s", position)
            raise NoCards(
                "You tried to draw from an empty deck. Position: %s", position
            )

    def draw(self) -> CardType:
        """
        Draw the topmost card from the deck

        :return:                Card from the list
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("top")

    def draw_bottom(self) -> CardType:
        """
        Draw the bottommost card from the deck

        :return:                Card from the list
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("bottom")

    def draw_random(self) -> CardType:
        """
        Draw a random card from the deck

        :return:                Card from the list
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        """
        return self._get_card("random")

    def draw_specific(self, specific_card: CardType) -> CardType:
        """
        Draw a specific card from the deck

        .. note::

            For card instances to match, they should have `__eq__`  method
            set to compare their equality. If you don't want to set those up,
            make sure their `__dict__` are the same and their name is the same.

            If you are using a string or an integer, don't worry about this!

        :param specific_card:   Card identical to the one you are looking for
        :return:                Card from the list
        :raises OutOfCards:     when there are no cards in the deck
        :raises NoCards:        when the deck runs out of cards (no reshuffle)
        :raises CardNotFound:   when the card is not found in the deck
        """
        log.debug("Attempting to find card: %s", specific_card)
        if self._cards:
            for available_card in self._cards:
                if _card_compare(specific_card, available_card):
                    card = available_card
                    break
            else:
                log.debug("Specific card not found in the deck")
                raise CardNotFound("Specific card not found in the deck")
            self._cards.remove(card)
            self.reshuffle_if_empty()
            log.debug("Specific card drawn: %s", card)
            return card

        else:
            log.debug("You tried to draw a specific card from an empty deck")
            raise NoCards("You tried to draw a specific card from an empty deck")

    def card_exists(self, card: CardType) -> bool:
        """
        Checks if a card exists in the deck

        .. note::

            For card instances to match, they should have `__eq__`  method
            set to compare their equality. If you don't want to set those up,
            make sure their `__dict__` are the same and their name is the same.

            If you are using a string or an integer, don't worry about this!

        :param card:    Card identical to the one you are looking for
        :return:        True if exists, False if doesn't exist
        """
        found = False
        for available_card in self._cards:
            if _card_compare(card, available_card):
                found = True
                break
        log.debug("Card %s exists in the deck: %s", card, found)
        return found

    def shuffle(self) -> None:
        """
        Randomizes the order of cards in the deck

        :raises NoCards:     when there are no cards to be shuffled
        """
        if self._cards:
            shuffle(self._cards)
            log.debug("Deck shuffled")
        else:
            log.warning("You tried to shuffle an empty deck")
            raise NoCards("You tried to shuffle an empty deck")

    def reshuffle_if_empty(self) -> None:
        """
        Function that checks if the deck is out of cards and if reshuffle is true, it
        shuffles the discard pile back into the card pile
        """
        if not self._cards and self._reshuffle:
            self.shuffle_back()

    def shuffle_back(self) -> None:
        """
        Shuffles the discard pile back into the main pile
        """
        for card in self._discard_pile:
            self._cards.append(card)
        self.shuffle()
        if isinstance(self._discard_pile, Deck):
            self._discard_pile.clear()
        else:
            self._discard_pile = []
        log.debug("Cards have been shuffled back from the discard pile")

    def discard(self, card: CardType) -> None:
        """
        Puts a card into the discard pile

        :param card:        Card to be discarded
        :raises NotACard:   When you try to insert False/None into a discard pile
        """
        log.debug("Card being discarded: %s", card)
        if card or type(card) == int:
            if isinstance(self._discard_pile, Deck):
                self._discard_pile.add_single(card, 0)
            else:
                self._discard_pile.append(card)
            log.debug("Card %s discarded", card)
        else:
            log.warning(
                "You tried to insert %s (rank(%s) into a discard pile",
                card,
                type(card).__name__,
            )
            raise NotACard(
                "You tried to insert {} (rank({}) into a discard pile".format(
                    card, type(card).__name__
                )
            )

    def clear(self) -> None:
        """
        Empties the deck, destroying contents
        """
        self._cards = []

    def add_single(self, card: CardType, position: int | None = None) -> None:
        """
        Shuffles (or inserts) a single card into the active deck

        :param card:        Card you want to insert
        :param position:    If you want to let player insert card to a specific location, use position
                            where 0 = top of the deck, 1 = second card from top etc.
                            By default the position is random.
        """
        if position is not None:
            self._cards.insert(position, card)
            log.debug("Card %s inserted to position %i", card, position)
            log.debug(self._cards)
        else:
            self._cards.insert(randint(0, len(self._cards)), card)
            log.debug("Card %s shuffled into the deck", card)

    def add_many(self, cards: list[CardType]) -> None:
        """
        Shuffles a list of cards into the deck

        :param cards:   Cards you want to shuffle in
        """
        for card in cards:
            self.add_single(card)
        log.debug("New cards shuffled into the deck")

    def show_top(self, number: int) -> list[CardType]:
        """
        Selects the top X cards from the deck without drawing them

        Useful for mechanics like scry in Magic The Gathering

        If there are less cards left than you want to show, it will show
        only the remaining cards

        :param number:      How many cards you want to show
        :return:            Cards you want to show
        """
        return self._cards[0:number]

    def set_file_location(self, location) -> None:
        """
        Used to update the location.
        It will expand relative file path and ~ if it exists.
        The file path should be relative to the main script.
        A filename must be passed in as part of location.

        Example: ~/mydeck.yml

        :param location: the location of the file
        """
        self._save_location = os.path.abspath(os.path.expanduser(location))

    def export(
        self, fmt: str, to_file: bool = False, location: str | None = None
    ) -> str:
        """
        Export the deck. By default it returns string with either JSON or YaML,
        but if you set `to_file=True`, you can instead save the deck as a file.
        If no location (with filename) is provided, it'll save to the folder the script
        is opened from as `exported_deck` without an extension.

        .. warning::

            The JSON export uses ``jsonpickle`` which serializes full Python objects.
            The YAML export uses ``yaml.dump`` which also serializes Python objects.
            These formats are **not safe to load from untrusted sources** as they can
            execute arbitrary code during deserialization. Only load data you have
            exported yourself or from sources you trust completely.

        :param fmt:             Desired format, either YaML or JSON
        :param to_file:         Whether you want to get a string back or save to a file
        :param location:        Where you want to save your file - include file name!
        :return:                Your exported deck as a string in your desired format
        :raises UnknownFormat:  When entered format is not supported
        """

        format_stripped = fmt.lower().strip()

        if location:
            self.set_file_location(location)
        else:
            self.set_file_location("exported_deck")

        # Hide location for security from exported deck
        temp_location = self._save_location
        self._save_location = None

        exported = _get_exported_string(format_stripped, self)

        self._save_location = temp_location

        if to_file:
            with open(self._save_location, "w") as target_file:
                target_file.writelines(exported)
            log.debug("File exported to: %s", self._save_location)

        return exported

    def load(self, to_load: str, is_file: bool = False) -> None:
        """
        Way to override a deck instance with a saved deck from either yaml, JSON
        or a file with either of those.

        .. warning::

            This method uses ``jsonpickle`` and ``yaml.unsafe_load`` to deserialize data,
            which can **execute arbitrary code**. Never call this with data from untrusted
            sources. Only load data you have exported yourself or from sources you trust
            completely.

        :param to_load:         This should be either a path to a file or a string containing
                                json/yaml generated by Deck.export().
        :param is_file:         whether to_load is a file path or actual data. Default is False
        :raises UnknownFormat:  When the entered yaml or json is not valid
        """
        if is_file:
            self.set_file_location(to_load)
            with open(self._save_location, "r") as file:
                loadable = file.read()
        else:
            loadable = to_load
        try:
            result = jsonpickle.decode(loadable)
            log.debug("loading JSON")
        except Exception:
            result = yaml.unsafe_load(loadable)
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

        with open(location) as f:
            data = yaml.unsafe_load(f).__dict__
        del data["_save_location"]
        self.__dict__.update(data)

    @property
    def cards_left(self) -> int:
        """
        :return:    Number of cards in the deck
        """
        return len(self._cards)

    @property
    def discarded(self) -> int:
        """
        :return:    Number of cards in the discard pile
        """
        return len(self._discard_pile)

    @property
    def json(self) -> str:
        """
        Alternative to Deck.export("json")

        .. warning::

            See :meth:`export` for security considerations.

        :return:    jsonpickled Deck
        """
        return self.export("json", to_file=False)

    @property
    def yaml(self) -> str:
        """
        Alternative to Deck.export("yaml")

        .. warning::

            See :meth:`export` for security considerations.

        :return:    yaml dump of the Deck
        """
        return self.export("yaml")

    @property
    def empty(self) -> bool:
        """
        :return:    Whether the deck is empty
        """
        return not self._cards

    @property
    def file_location(self) -> str:
        """
        :return:    The file location from which current deck is loaded from / will be saved to
        """
        return self._save_location

    def __repr__(self) -> str:  # pragma: no cover
        return "Deck(cards={0}, discarded={3}, reshuffle={1}, name={2})".format(
            self.cards_left, self._reshuffle, self.name, self.discarded
        )

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return "Deck of cards"

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position: int) -> CardType:
        return self._cards[position]

    def __setitem__(self, position: int, card: CardType) -> None:
        self._cards[position] = card

    def __iter__(self) -> Iterator[CardType]:
        return iter(self._cards)


def _card_compare(card: CardType, second_card: CardType) -> bool:
    """
    Function for comparing two cards. First it checks their `__eq__`,
    if that returns False, it checks `__dict__` and name of the Class
    that spawned them.
    """
    identity = False
    if second_card == card:
        identity = True
    else:
        try:
            if (
                second_card.__dict__ == card.__dict__
                and type(second_card).__name__ == type(card).__name__
            ):
                identity = True
        except AttributeError:
            pass
    return identity


def _get_exported_string(format_stripped: str, deck: Deck) -> str:
    """
    Helper function to Deck.export()

    :param format_stripped:     Desired format stripped of any spaces and lowercase
    :param deck:                instance of a Deck
    :return:                    YAML/JSON string of the deck
    :raises UnknownFormat:      when it doesn't recognize format_stripped
    """
    if format_stripped in ("yaml", "yml"):
        exported = yaml.dump(deck)
        log.debug("Exported deck %r to a yaml string", deck)
    elif format_stripped == "json":
        exported = jsonpickle.encode(deck)
        log.debug("Exported deck %r to a json string", deck)
    else:
        log.debug("Unknown format: %s", format_stripped)
        raise UnknownFormat(f"Unknown format: {format_stripped}")
    return exported
