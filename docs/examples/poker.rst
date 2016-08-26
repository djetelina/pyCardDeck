Poker example
=============


This is a poker example of pyCardDeck, it's not meant to be complete poker script,
but rather a showcase of pyCardDeck's usage.

.. code-bloack:: python

    import pyCardDeck
    from typing import List
    from pyCardDeck.cards import PokerCard

For python 3.3 and 3.4 compatibility and type hints, we import typing.List - this is not needed, however
the package itself and PokerCard are recommended here


.. code-bloack:: python

    class Player:

        def __init__(self, name: str):
            self.hand = []
            self.name = name

        def __str__(self):
            return self.name


    class PokerTable:

        def __init__(self, players: List[Player]):
            self.deck = pyCardDeck.Deck(
                cards=generate_deck(),
                name='Poker deck',
                reshuffle=False)
            self.players = players
            self.table_cards = []
            print("Created a table with {} players".format(len(self.players)))

We define our Player class, to have a hand and a name, and our PokerTable which will hold all the information
and will have following methods:

.. code-bloack:: python

        def texas_holdem(self):
            """
            Basic Texas Hold'em game structure
            """
            print("Starting a round of Texas Hold'em")
            self.deck.shuffle()
            self.deal_cards(2)
            # Imagine pre-flop logic for betting here
            self.flop()
            # Imagine post-flop, pre-turn logic for betting here
            self.river_or_flop()
            # Imagine post-turn, pre-river logic for betting here
            self.river_or_flop()
            # Imagine some more betting and winner decision here
            self.cleanup()

This is the core "loop" of Texas Hold'em


.. code-bloack:: python

        def deal_cards(self, number: int):
            for _ in range(0, number):
                for player in self.players:
                    card = self.deck.draw()
                    player.hand.append(card)
                    print("Dealt {} to player {}".format(card, player))

Dealer will go through all available players and deal them x number of cards.


.. code-bloack:: python

        def flop(self):
            # Burn a card
            burned = self.deck.draw()
            self.deck.discard(burned)
            print("Burned a card: {}".format(burned))
            for _ in range(0, 3):
                card = self.deck.draw()
                self.table_cards.append(card)
                print("New card on the table: {}".format(card))


Burns a card and then shows 3 new cards on the table

.. code-bloack:: python

        def river_or_flop(self):
            burned = self.deck.draw()
            self.deck.discard(burned)
            print("Burned a card: {}".format(burned))
            card = self.deck.draw()
            self.table_cards.append(card)
            print("New card on the table: {}".format(card))


Burns a card and then shows 1 new card on the table

.. code-bloack:: python

        def cleanup(self):
            for player in self.players:
                for card in player.hand:
                    self.deck.discard(card)
            for card in self.table_cards:
                self.deck.discard(card)
            self.deck.shuffle_back()
            print("Cleanup done")


Cleans up the table to gather all the cards back

.. code-bloack:: python

    def generate_deck() -> List[PokerCard]:
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = {'A': 'Ace',
                 '2': 'Two',
                 '3': 'Three',
                 '4': 'Four',
                 '5': 'Five',
                 '6': 'Six',
                 '7': 'Seven',
                 '8': 'Eight',
                 '9': 'Nine',
                 '10': 'Ten',
                 'J': 'Jack',
                 'Q': 'Queen',
                 'K': 'King'}
        cards = []
        for suit in suits:
            for rank, name in ranks.items():
                cards.append(PokerCard(suit, rank, name))
        print('Generated deck of cards for the table')
        return cards\


Function that generates the deck, instead of writing down 50 cards, we use iteration to generate the cards for use

.. code-bloack:: python

    if __name__ == '__main__':
        table = PokerTable([Player("Jack"), Player("John"), Player("Peter")])
        table.texas_holdem()

And finally this is how we start the "game"