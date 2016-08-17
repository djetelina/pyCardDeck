from unittest import TestCase
from pyCardDeck import Deck


class Card:
    def __init__(self, name: str):
        self.name = name


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
        d.draw()
        self.assertTrue(d.empty)

    def test_draw_else(self):
        d = Deck()
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
        d.draw()
        self.assertTrue(d.empty)
        d = Deck()
        d.draw()
        self.assertTrue(d.empty)

    def test_draw_random(self):
        pass

    def test_draw_specific(self):
        pass

    def test_card_exists(self):
        pass

    def test_shuffle(self):
        pass

    def test_shuffle_back(self):
        pass

    def test_discard(self):
        pass

    def test_add_single(self):
        pass

    def test_add_many(self):
        pass

    def test_show_top(self):
        pass

    def test_cards_left(self):
        pass

    def test_discarded(self):
        pass
