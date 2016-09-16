pyCardDeck
==========

Status
------

.. list-table::
    :widths: 30 30

    * - License
      -     .. image:: https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000
                :target: https://opensource.org/licenses/MIT
                :alt: MIT License
    * - Versioning
      -     .. image:: https://badge.fury.io/py/pyCardDeck.svg
                :target: https://badge.fury.io/py/pyCardDeck
                :alt: pypi
            .. image:: https://requires.io/github/iScrE4m/pyCardDeck/requirements.svg?branch=master
                 :target: https://requires.io/github/iScrE4m/pyCardDeck/requirements/?branch=master
                 :alt: Requirements Status
    * - Documentation
      -     .. image:: https://readthedocs.org/projects/pycarddeck/badge/?version=latest
                :target: http://pycarddeck.readthedocs.io/en/latest/?badge=latest
                :alt: Documentation Status
    * - Tests
      -     .. image:: https://travis-ci.org/iScrE4m/pyCardDeck.svg?branch=master
                :target: https://travis-ci.org/iScrE4m/pyCardDeck
                :alt: Travis CI
            .. image:: https://codeclimate.com/github/iScrE4m/pyCardDeck/badges/coverage.svg
               :target: https://codeclimate.com/github/iScrE4m/pyCardDeck/coverage
               :alt: Test Coverage
    * - Code Quality
            .. image:: https://codeclimate.com/github/iScrE4m/pyCardDeck/badges/gpa.svg
               :target: https://codeclimate.com/github/iScrE4m/pyCardDeck
               :alt: Code Climate
            .. image:: https://codeclimate.com/github/iScrE4m/pyCardDeck/badges/issue_count.svg
               :target: https://codeclimate.com/github/iScrE4m/pyCardDeck
               :alt: Issue Count

Library aimed at anyone who wants to do any kind of deck manipulation in python.
So probably game developers. The goal is to have the ultimate library for all of this,
supporting all kinds of game types with clean and beautiful API - kind of like requests :)

How to use
----------

First, install with pip::

    pip install pyCardDeck

Then use in your code:

.. code-block:: python

    import pyCardDeck

    my_deck = pyCardDeck.Deck(cards=[1, 2, 3], name='My Awesome Deck')

    my_deck.shuffle()

    card = my_deck.draw()

For more elaborate examples check out `GitHub <https://github.com/iScrE4m/pyCardDeck/tree/master/examples>`_

For developers
--------------

The library will support Python 3.3+, for requirements look at requirements.txt in the repository.

This library should be very easy to contribute to for first timers. Nothing is sacred, File issues, contribute
where you feel it's useful and fun for you!

Always aim to write clean and readable code, make sure the tests are passing, document in docstrings (rst format)
and when writing new modules, classes or functions, add them to docs (we are using Shpinx autodocs)

Running tests
~~~~~~~~~~~~~

To run tests enter the pyCardDeck directory and run::

    py.test tests
