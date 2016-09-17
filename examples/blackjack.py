#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a blackjack game made with pyCardDeck, meant as an example rather than
as a complete game.
"""

import sys
import pyCardDeck
from typing import List
from pyCardDeck.cards import PokerCard

# Copy-pasted from examples/poker.py
class Player:

    def __init__(self, name: str):
        self.hand = []
        self.name = name

    def __str__(self):
        return self.name

class BlackjackGame:

    def __init__(self, players: List[Player]):
        self.deck = pyCardDeck.Deck(
            cards=generate_deck(),
            name='Poker deck',
            reshuffle=False)
        self.players = players
        self.scores = {}
        print("Created a game with {} players.".format(len(self.players)))

    def blackjack(self):
        """
        The main blackjack game sequence.

        Each player takes an entire turn before moving on.

        If each player gets a turn and no one has won, the player or players
        with the highest score below 21 are declared the winner.
        """
        print("Setting up...")
        print("Shuffling...")
        self.deck.shuffle()
        print("All shuffled!")
        print("Dealing...")
        self.deal()
        print("\nLet's play!")
        for player in self.players:
            print("{}'s turn...".format(player.name))
            self.play(player)
        else:
            print("That's the last turn. Determining the winner...")
            self.find_winner()

    def play(self, player):
        """
        An individual player's turn.

        If the player's cards are an ace and a ten or court card,
        the player has a blackjack and wins.

        If a player's cards total more than 21, the player loses.

        Otherwise, it takes the sum of their cards and determines whether
        to hit or stand based on their current score.
        """
        while True:
            points = sum_hand(player.hand)
            if points < 17:
                print("   Hit.")
                self.hit(player)
            elif points == 21:
                print("   {} wins!".format(player.name))
                sys.exit(0) # End if someone wins
            elif points > 21:
                print("   Bust!")
                break
            else:  # Stand if between 17 and 20 (inclusive)
                print("   Standing at {} points.".format(str(points)))
                self.scores[player.name] = points
                break

    def find_winner(self):
        """
        Finds the highest score, then finds which player(s) have that score,
        and reports them as the winner.
        """
        winners = []
        try:
            win_score = max(self.scores.values())
            for key in self.scores.keys():
                if self.scores[key] == win_score:
                    winners.append(key)
                else:
                    pass
            winstring = " & ".join(winners)
            print("And the winner is...{}!".format(winstring))
        except ValueError:
            print("Whoops! Everybody lost!")

    def deal(self):
        """
        Deals two cards to each player.
        """
        # i = 1
        # while i <= 2:
        for _ in range(2):
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.append(newcard)
                print("Dealt {} the {}.".format(p.name, str(newcard)))
            # i += 1


    def hit(self, player):
        """
        Adds a card to the player's hand and states which card was drawn.
        """
        newcard = self.deck.draw()
        player.hand.append(newcard)
        print("   Drew the {}.".format(str(newcard)))


def sum_hand(hand: list):
    """
    Converts ranks of cards into point values for scoring purposes.
    'K', 'Q', and 'J' are converted to 10.
    'A' is converted to 1 (for simplicity), but if the first hand is an ace
    and a 10-valued card, the player wins with a blackjack.
    """
    vals = [card.rank for card in hand]
    for i in range(0, len(vals)):
        try:
            vals[i] = int(vals[i])
        except ValueError:
            if vals[i] in ['K', 'Q', 'J']:
                vals[i] = 10
            elif vals[i] == 'A':
                vals[i] = 1  # Keep it simple for the sake of example
    if vals == [1, 10] or vals == [10, 1]:
        print("   Blackjack!")
        return(21)
    else:
        points = sum(vals)
        print("   Current score: {}".format(str(points)))
        return(points)

# Copy-pasted from examples/poker.py
def generate_deck() -> List[PokerCard]:
    """
    Function that generates the deck, instead of writing down 50 cards, we use iteration
    to generate the cards for use

    :return:    List with all 50 poker playing cards
    :rtype:     List[PokerCard]
    """
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
    print('Generated deck of cards for the table.')
    return cards

if __name__ == "__main__":
    game = BlackjackGame([Player("Kit"), Player("Anya"), Player("Iris"),
        Player("Simon")])
    game.blackjack()
