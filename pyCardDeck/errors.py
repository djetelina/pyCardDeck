# -*- coding: utf-8 -*-


class DeckException(Exception):
    """
    Base exception class for pyCardDeck
    """
    pass


class NoCards(DeckException):
    """
    Exception that's thrown when there are no cards to be manipulated.
    """
    pass


class OutOfCards(DeckException):
    """
    Exception that's thrown when the deck runs out of cards.
    Unlike NoCardsException, this will happen naturally when reshuffling is disabled
    """
    pass


class NotACard(DeckException):
    """
    Exception that's thrown when the manipulated object is False/None
    """
    pass


class CardNotFound(DeckException):
    """
    Exception that's thrown when a card is not found
    """
    pass


class UnknownFormat(Exception):
    """
    Exception thrown when trying to export to a unknown format.
    Supported formats: YaML, JSON
    """
    pass
