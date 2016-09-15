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
# from pyCardDeck.cards import PokerCard
from pyCardDeck.examples import poker #generate_deck

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
            cards=poker.generate_deck(),
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

    def play(self):
        while True:
            points = sum_hand(player.hand)
            print("\tCurrent score: {}".format(str(points)))
            if points < 17:
                print("\tHit.")
                hit(player)
            elif points == 21:
                print("\t{} wins!".format(player.name))
                # break
                sys.exit(0) # End if someone wins
            elif points > 21:
                print("\tBust!")
                # player.playing = False
                break
            else:  # Stand if between 17 and 20 (inclusive)
                print("\tStanding at {} points.".format(str(points)))
                self.scores[player.name] = points
                break

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
                self.players.hand.append(newcard)
                print("Dealt {} a {}.".format(p, str(newcard)))
            i += 1


def hit(player):
    newcard = self.deck.draw()
    self.players.hand.append(newcard)
    print("\tDrew a {}.".format(p, str(newcard)))


def sum_hand(hand):
    # hand = player.hand
    vals = [card.rank for card in hand]
    for i in range(0, len(vals)):
        try:
            vals[i] = int(vals[i])
        except TypeError:
            if vals[i] in ['K', 'Q', 'J']:
                vals[i] = 10
            elif vals[i] == 'A':
                vals[i] = 1  # Keep it simple for the sake of example
    if vals == [1, 10] or [10, 1]:
        print("\tBlackjack!")
        return(21)
    else:
        return(sum(vals))
