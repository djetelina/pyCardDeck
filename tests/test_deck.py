#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from pyCardDeck import *


class Card:
    """
    Example Card object, will be replaced by template later down the line
    """

    def __init__(self, name: str, specific_string="abc"):
        self.name = name
        self.specific_string = specific_string

    def __str__(self):
        return "Card instance {0.name}, {0.specific_string}" \
            .format(self)


class DifferentCard(Card):
    """
    Card object that's a different class than card
    """


class TestDeck(TestCase):
    def test_draw(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        self.assertEqual(d.draw().name, Card('One').name)
        self.assertEqual(d.draw().name, Card('Two').name)
        self.assertEqual(d.draw().name, Card('Three').name)
        self.assertEqual(d.draw().name, Card('Four').name)
        self.assertTrue(d.empty)
        with self.assertRaises(OutOfCards):
            d.draw()
        self.assertTrue(d.empty)

    def test_draw_bottom(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        self.assertEqual(d.draw_bottom().name, Card('Four').name)
        self.assertEqual(d.draw_bottom().name, Card('Three').name)
        self.assertEqual(d.draw_bottom().name, Card('Two').name)
        self.assertEqual(d.draw_bottom().name, Card('One').name)
        self.assertTrue(d.empty)
        with self.assertRaises(OutOfCards):
            d.draw_bottom()
        self.assertTrue(d.empty)

    def test_draw_random(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.draw_random()
        d.draw_random()
        d.draw_random()
        d.draw_random()
        self.assertTrue(d.empty)
        with self.assertRaises(OutOfCards):
            d.draw_random()
        self.assertTrue(d.empty)

    def test_draw_specific_instance(self):
        one = Card('One', specific_string="bbc")
        one_small = Card('one', specific_string="bbc")
        one_diff_string = Card('One', specific_string="car")
        one_bare = Card('One')
        d = Deck(cards=[
            one,
            one_small,
            one_diff_string,
            one_bare
        ], reshuffle=False)
        self.assertEqual(d.draw_specific(one).__dict__, one.__dict__)
        with self.assertRaises(CardNotFound):
            d.draw_specific(Card('Seven'))
        d.draw_specific(one_small)
        d.draw_specific(one_diff_string)
        d.draw_specific(one_bare)
        self.assertTrue(d.empty)
        with self.assertRaises(NoCards):
            d.draw_specific(one_bare)

    def test_draw_specific_string(self):
        d = Deck(cards=['a', 'b', 'c', 'd'])
        self.assertEqual(d.draw_specific('a'), 'a')

    def test_draws_else(self):
        d = Deck()
        with self.assertRaises(NoCards):
            d.draw()
        self.assertTrue(d.empty)
        with self.assertRaises(NoCards):
            d.draw_bottom()
        self.assertTrue(d.empty)
        with self.assertRaises(NoCards):
            d.draw_random()
        self.assertTrue(d.empty)

    def test_draws_reshuffle(self):
        d = Deck(cards=[Card('One')])
        d.discard(Card('One'))
        d.draw_specific(Card('One'))
        self.assertFalse(d.empty)
        d.discard(Card('One'))
        d.draw()
        self.assertFalse(d.empty)
        d.discard(Card('One'))
        d.draw_bottom()
        self.assertFalse(d.empty)
        d.discard(Card('One'))
        d.draw_random()
        self.assertFalse(d.empty)

    def test_card_exists_instance(self):
        one = Card('One', specific_string='bbc')
        one_alt = DifferentCard('One', specific_string='bbc')
        d = Deck(cards=[
            one,
            Card('one', specific_string='bbc'),
            Card('One', specific_string='car'),
            Card('One')
        ], reshuffle=False)
        self.assertTrue(d.card_exists(one))
        # noinspection PyPep8
        assert False == d.card_exists(one_alt)
        self.assertFalse(d.card_exists(Card('Five')))

    def test_card_exist_string(self):
        d = Deck(cards=['a', 'b', 'c', 'd'])
        self.assertTrue(d.card_exists('a'))
        self.assertFalse(d.card_exists('z'))

    def test_shuffle(self):
        d = Deck()
        with self.assertRaises(NoCards):
            d.shuffle()

    def test_discard(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.discard(Card('One'))
        d.discard(Card('Two'))
        self.assertEqual(d.discarded, 2)
        with self.assertRaises(NotACard):
            d.discard(False)
        self.assertEqual(d.discarded, 2)
        d.discard(0)
        assert d.discarded == 3

    def test_shuffle_back(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.draw()
        d.draw()
        self.assertEqual(len(d), 2)
        d.discard(Card('One'))
        d.discard(Card('Two'))
        d.shuffle_back()
        self.assertEqual(len(d), 4)

    def test_add_single(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.add_single(Card('Five'))
        self.assertEqual(len(d), 5)

    def test_add_many(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.add_many([Card('Five'), Card('Six')])
        self.assertEqual(len(d), 6)

    def test_show_top_one(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        self.assertEqual(d.show_top(1)[0].__dict__, Card('One').__dict__)

    def test_show_top_three(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        self.assertEqual(d.show_top(3)[0].__dict__, Card('One').__dict__)
        self.assertEqual(d.show_top(3)[1].__dict__, Card('Two').__dict__)
        self.assertEqual(d.show_top(3)[2].__dict__, Card('Three').__dict__)

    def test_cards_left(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        assert d.cards_left == 4

    def test_cards_left_empty(self):
        d = Deck()
        assert d.cards_left == 0

    def test_discarded(self):
        d = Deck(cards=[
            Card('One'), Card('Two'), Card('Three'), Card('Four')
        ], reshuffle=False)
        d.discard(d.draw())
        d.discard(d.draw_bottom())
        self.assertEqual(d.discarded, 2)

    def test__repr__(self):
        d = Deck()
        self.assertEqual('Deck(cards=0, discarded=0, reshuffle=True, name=None)',
                         repr(d))
        d = Deck(cards=[Card('One'), Card('Two'), Card('Three')], reshuffle=False, name='Deck')
        d.discard(Card('Four'))
        self.assertEqual('Deck(cards=3, discarded=1, reshuffle=False, name=Deck)',
                         repr(d))

    def test__str__named(self):
        d = Deck(name='SuperDeck')
        assert 'SuperDeck' == str(d)

    def test__str__(self):
        d = Deck()
        assert 'Deck of cards' == str(d)
