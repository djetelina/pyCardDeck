# pyCardDeck

[![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/pyCardDeck.svg)](https://badge.fury.io/py/pyCardDeck)

Library aimed at anyone who wants to do any kind of deck manipulation in python.
So probably game developers. The goal is to have the ultimate library for all of this,
supporting all kinds of game types with clean and beautiful API - kind of like requests :)

## How to use

First, install with pip:

```
pip install pyCardDeck
```

Then use in your code:

```python
import pyCardDeck

my_deck = pyCardDeck.Deck(cards=[1, 2, 3], name='My Awesome Deck')

my_deck.shuffle()

card = my_deck.draw()
```

For more elaborate examples check out [GitHub](https://github.com/djetelina/pyCardDeck/tree/master/examples)

Full documentation is available on [ReadTheDocs](https://pycarddeck.readthedocs.io).

## For developers

The library supports Python 3.10+.

This library should be very easy to contribute to for first timers. Nothing is sacred, file issues, contribute
where you feel it's useful and fun for you! If you need help, just ask.

Always aim to write clean and readable code, make sure the tests are passing, document in docstrings (rst format)
and when writing new modules, classes or functions, add them to docs (we are using Sphinx autodocs)

### Running tests

To run tests enter the pyCardDeck directory and run:

```
uv run pytest
```
