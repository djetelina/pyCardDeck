.. pyCardDeck documentation master file, created by
   sphinx-quickstart on Wed Aug 17 20:12:10 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyCardDeck's documentation!
======================================

.. automodule:: pyCardDeck

   .. autoclass:: Deck

      .. rubric:: Attributes

      .. py:attribute:: name

         :return: The name of the deck
         :rtype:  str

      .. py:attribute:: cards

         :return: Cards in the deck
         :rtype: list

      .. py:attribute:: discard_pile

         :return: Cards in the discard pile
         :rtype: list

      .. py:attribute:: empty

         :return: Whether the deck is empty
         :rtype:  bool

      .. py:attribute:: reshuffle

         :return: Whether the deck will be reshuffled when drawn out
         :rtype:  bool

      .. autoattribute:: cards_left

      .. autoattribute:: discarded

      .. rubric:: Cards drawing

      .. automethod:: draw

      .. automethod:: draw_bottom

      .. automethod:: draw_random

      .. automethod:: draw_specific

      .. rubric:: Deck Manipulation

      .. automethod:: shuffle

      .. automethod:: shuffle_back

      .. automethod:: discard

      .. automethod:: add_single

      .. automethod:: add_many

      .. automethod:: show_top

      .. rubric:: Magic Methods

      .. automethod:: __repr__

      .. automethod:: __str__

      .. automethod:: __len__

Exceptions
==========

.. automodule:: pyCardDeck.errors

.. autoexception:: DeckException

.. autoexception:: NoCards

.. autoexception:: OutOfCards

.. autoexception:: NotACard

.. autoexception:: CardNotFound


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

