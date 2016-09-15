#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a blackjack game made with pyCardDeck, meant as an example rather than
as a complete game.
"""

import sys
import pyCardDeck
# noinspection PyCompatibility
from typing import List
from pyCardDeck.cards import PokerCard
# from pyCardDeck.examples import poker #generate_deck

class Player:

    def __init__(self, name: str):
        self.hand = []
        self.name = name
        # self.playing = True

    def __str__(self):
        return self.name

class BlackjackGame:

    def __init__(self, players: List[Player]):
        self.deck = pyCardDeck.Deck(
            cards=generate_deck(),
            name='Poker deck',
            reshuffle=False)
        self.players = players
        # self.table_cards = []
        self.scores = {}
        # self.winners = []
        print("Created a game with {} players".format(len(self.players)))

    def blackjack(self):
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
            print("That's the last turn. Calculating the winner...")
            self.find_winner()

    def play(self, player):
        while True:
            points = sum_hand(player.hand)
            # print("   Current score: {}".format(str(points)))
            if points < 17:
                print("   Hit.")
                self.hit(player)
            elif points == 21:
                print("   {} wins!".format(player.name))
                # break
                sys.exit(0) # End if someone wins
            elif points > 21:
                print("   Bust!")
                # player.playing = False
                break
            else:  # Stand if between 17 and 20 (inclusive)
                print("   Standing at {} points.".format(str(points)))
                self.scores[player.name] = points
                break

    def find_winner(self):
        winners = []
        win_score = max(self.scores.values())
        for key in self.scores.keys():
            if self.scores[key] == win_score:
                winners.append(key)
            else:
                None
        winstring = " & ".join(winners)
        if winstring == '':
            print("Whoops! Everybody lost!")
        else:
            print("And the winner is...{}!".format(winstring))

    def deal(self):
        i = 1
        while i <= 2:
            for p in self.players:
                newcard = self.deck.draw()
                p.hand.append(newcard)
                print("Dealt {} the {}.".format(p.name, str(newcard)))
            i += 1


    def hit(self, player):
        newcard = self.deck.draw()
        player.hand.append(newcard)
        print("   Drew the {}.".format(str(newcard)))


def sum_hand(hand: list): 
    # hand = player.hand
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
    print('Generated deck of cards for the table')
    return cards

if __name__ == "__main__":
    game = BlackjackGame([Player("Davar"), Player("Squiggletoe"),
        Player("Knife Emoji"), Player("Simon")])
    game.blackjack()
