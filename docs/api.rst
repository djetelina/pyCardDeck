API
===

.. automodule:: pyCardDeck

Types
=====

pyCardDeck isn't strict about types. It's however nice to use Python 3's type annotations.
That's why we have custom types set up when needed

.. _CardType:

CardType
--------

Can be either instance of an object, string or an integer. Basically, it's important
that they aren't bool or NoneType. It's however recommended to inherit from
one of the classes in :ref:`Cards`

Classes and Functions
=====================

Deck
----

.. autoclass:: pyCardDeck.deck.Deck

Attributes
~~~~~~~~~~

.. py:attribute:: Deck.name

    :return: The name of the deck
    :rtype:  str

.. py:attribute:: Deck.reshuffle

    :return: Whether the deck will be reshuffled when drawn out
    :rtype:  bool

.. py:attribute:: Deck._cards

    :return: Cards in the deck
    :rtype: list

.. py:attribute:: Deck._discard_pile

    .. note::

        Cards are not put in the discard pile automatically after drawing,
        the code assumes they went into a hand of sorts and must be discarded
        with :py:func:`discard` from there. This means that :py:attr:`reshuffle` doesn't
        work on one card deck as you can't reshuffle an empty deck
        (:py:exc:`errors.NoCards` would be raised).

    :return: Cards in the discard pile
    :rtype: list

.. autoattribute:: pyCardDeck.deck.Deck.empty

.. autoattribute:: pyCardDeck.deck.Deck.cards_left

.. autoattribute:: pyCardDeck.deck.Deck.discarded

.. autoattribute:: pyCardDeck.deck.Deck.json

.. autoattribute:: pyCardDeck.deck.Deck.yaml

Card drawing
~~~~~~~~~~~~

.. automethod:: pyCardDeck.deck.Deck.draw

.. automethod:: pyCardDeck.deck.Deck.draw_bottom

.. automethod:: pyCardDeck.deck.Deck.draw_random

.. automethod:: pyCardDeck.deck.Deck.draw_specific

Card information
~~~~~~~~~~~~~~~~

.. automethod:: pyCardDeck.deck.Deck.card_exists

Deck Manipulation
~~~~~~~~~~~~~~~~~

.. automethod:: pyCardDeck.deck.Deck.shuffle

.. automethod:: pyCardDeck.deck.Deck.shuffle_back

.. automethod:: pyCardDeck.deck.Deck.discard

.. automethod:: pyCardDeck.deck.Deck.add_single

.. automethod:: pyCardDeck.deck.Deck.add_many

.. automethod:: pyCardDeck.deck.Deck.show_top

Import/Export
~~~~~~~~~~~~~

.. automethod:: pyCardDeck.deck.Deck.export

.. automethod:: pyCardDeck.deck.Deck.load

.. automethod:: pyCardDeck.deck.Deck.load_standard_deck

Magic Methods
~~~~~~~~~~~~~

.. automethod:: pyCardDeck.deck.Deck.__repr__

.. automethod:: pyCardDeck.deck.Deck.__str__

.. automethod:: pyCardDeck.deck.Deck.__len__

Other Functions
~~~~~~~~~~~~~~~

.. autofunction:: pyCardDeck.deck.card_compare

.. autofunction:: pyCardDeck.deck.get_exported_string

.. _Cards:

Cards
-----

These classes are only recommended to inherit from, feel free to use your own!

.. autoclass:: pyCardDeck.cards.BaseCard

.. autoclass:: pyCardDeck.cards.PokerCard

Exceptions
----------

.. automodule:: pyCardDeck.errors

.. autoexception:: DeckException

.. autoexception:: NoCards

.. autoexception:: OutOfCards

.. autoexception:: NotACard

.. autoexception:: CardNotFound

.. autoexception:: UnknownFormat
