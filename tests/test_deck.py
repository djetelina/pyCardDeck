#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from pyCardDeck import *


class Card:
    """
    Example Card object, will be replaced by template later down the line
    """

    def __init__(self, name: str, specific_string="abc"):
        self.name = name
        self.specific_string = specific_string

    def __repr__(self):
        return "Card instance {0.name}, {0.specific_string}" \
            .format(self)


class DifferentCard(Card):
    """
    Card object that's a different class than card
    """


class ExportCard(Card):
    """
    Card object used for importing and exporting
    """

    def __eq__(self, other):
        return self.name == other


def test_draw():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    assert d.draw().name == Card('One').name
    d.draw()
    d.draw()
    assert d.draw().name == Card('Four').name
    with pytest.raises(OutOfCards):
        d.draw()
    assert True == d.empty


# noinspection PyPep8
def test_draw_bottom():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.draw_bottom()
    assert d.draw_bottom().name == Card('Three').name
    d.draw_bottom()
    assert d.draw_bottom().name == Card('One').name
    with pytest.raises(OutOfCards):
        d.draw_bottom()
    assert True == d.empty


# noinspection PyPep8,PyPep8
def test_draw_random():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.draw_random()
    d.draw_random()
    d.draw_random()
    d.draw_random()
    assert True == d.empty
    with pytest.raises(OutOfCards):
        d.draw_random()
    assert True == d.empty


# noinspection PyPep8
def test_draw_specific_instance():
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
    assert d.draw_specific(one).__dict__ == one.__dict__
    with pytest.raises(CardNotFound):
        d.draw_specific(Card('Seven'))
    d.draw_specific(one_small)
    d.draw_specific(one_diff_string)
    d.draw_specific(one_bare)
    assert True == d.empty
    with pytest.raises(NoCards):
        d.draw_specific(one_bare)


def test_draw_specific_string():
    d = Deck(cards=['a', 'b', 'c', 'd'])
    assert d.draw_specific('a') == 'a'


# noinspection PyPep8
def test_draws_else():
    d = Deck()
    with pytest.raises(NoCards):
        d.draw()
    with pytest.raises(NoCards):
        d.draw_bottom()
    with pytest.raises(NoCards):
        d.draw_random()
    assert True == d.empty


# noinspection PyPep8,PyPep8,PyPep8,PyPep8
def test_draws_reshuffle():
    d = Deck(cards=[Card('One')])
    d.discard(Card('One'))
    d.draw_specific(Card('One'))
    assert False == d.empty
    d.discard(Card('One'))
    d.draw()
    assert False == d.empty
    d.discard(Card('One'))
    d.draw_bottom()
    assert False == d.empty
    d.discard(Card('One'))
    d.draw_random()
    assert False == d.empty


# noinspection PyPep8,PyPep8
def test_card_exists_instance():
    one = Card('One', specific_string='bbc')
    one_alt = DifferentCard('One', specific_string='bbc')
    d = Deck(cards=[
        one,
        Card('one', specific_string='bbc'),
        Card('One', specific_string='car'),
        Card('One')
    ], reshuffle=False)
    assert True == d.card_exists(one)
    # noinspection PyPep8
    assert False == d.card_exists(one_alt)
    assert False == d.card_exists(Card('Five'))


# noinspection PyPep8,PyPep8
def test_card_exist_string():
    d = Deck(cards=['a', 'b', 'c', 'd'])
    assert True == d.card_exists('a')
    assert False == d.card_exists('z')


def test_shuffle():
    d = Deck()
    with pytest.raises(NoCards):
        d.shuffle()


def test_discard():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.discard(Card('One'))
    d.discard(Card('Two'))
    assert d.discarded == 2
    with pytest.raises(NotACard):
        d.discard(False)
    assert d.discarded == 2
    d.discard(0)
    assert d.discarded == 3


def test_shuffle_back():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.draw()
    d.draw()
    assert len(d) == 2
    d.discard(Card('One'))
    d.discard(Card('Two'))
    d.shuffle_back()
    assert len(d) == 4


def test_add_single():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.add_single(Card('Five'))
    assert len(d) == 5


def test_add_many():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.add_many([Card('Five'), Card('Six')])
    assert len(d) == 6


def test_show_top_one():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    assert d.show_top(1)[0].__dict__ == Card('One').__dict__


def test_show_top_three():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    assert d.show_top(3)[0].__dict__, Card('One').__dict__
    assert d.show_top(3)[1].__dict__, Card('Two').__dict__
    assert d.show_top(3)[2].__dict__, Card('Three').__dict__


def test_cards_left():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    assert d.cards_left == 4


def test_cards_left_empty():
    d = Deck()
    assert d.cards_left == 0


def test_discarded():
    d = Deck(cards=[
        Card('One'), Card('Two'), Card('Three'), Card('Four')
    ], reshuffle=False)
    d.discard(d.draw())
    d.discard(d.draw_bottom())
    assert d.discarded, 2


def test__repr__():
    d = Deck()
    assert 'Deck(cards=0, discarded=0, reshuffle=True, name=None)', repr(d)
    d = Deck(cards=[Card('One'), Card('Two'), Card('Three')], reshuffle=False, name='Deck')
    d.discard(Card('Four'))
    assert 'Deck(cards=3, discarded=1, reshuffle=False, name=Deck)', repr(d)


def test__str__named():
    d = Deck(name='SuperDeck')
    assert 'SuperDeck' == str(d)


def test__str__():
    d = Deck()
    assert 'Deck of cards' == str(d)


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_yaml_import_export_ints():
    d = Deck(cards=[1, 2, 3, 4], name="Test yaml int")
    d.export(" yaMl ", to_file=True, location="tests/test_int.yaml")
    e = Deck()
    e.load("tests/test_int.yaml", is_file=True)
    assert e._cards == d._cards
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_yaml_import_export_strings():
    d = Deck(cards=["one", "two", "three", 'four', '5', '6'], name="Test yaml str")
    d.export("YAML", to_file=True, location="tests/test_str.yaml")
    e = Deck()
    e.load("tests/test_str.yaml", is_file=True)
    assert e._cards == d._cards
    assert d._save_location == e.file_location
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_yaml_import_export_base_card():
    d = Deck(cards=[BaseCard("One"), BaseCard("Two"), BaseCard("Three"), BaseCard("Four")],
             name="Test yaml basecard")
    d.export("yaml ", to_file=True, location="tests/test_basecard.yaml")
    e = Deck()
    e.load("tests/test_basecard.yaml", is_file=True)
    assert e._cards[0].__dict__ == d._cards[0].__dict__
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_yaml_import_export_custom_card():
    d = Deck(cards=[ExportCard("One"), ExportCard("Two"), ExportCard("Three")], name="Test yaml custom")
    d.export("   YaML", to_file=True, location="tests/test_custom.yaml")
    e = Deck(name="This will get overriden")
    e.load("tests/test_custom.yaml", is_file=True)
    assert e._cards == d._cards
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_json_import_export_ints():
    d = Deck(cards=[1, 2, 3, 4], name="Test json int")
    d.export(" Json ", to_file=True, location="tests/test_int.json")
    e = Deck()
    e.load("tests/test_int.json", is_file=True)
    assert e._cards == d._cards
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_json_import_export_strings():
    d = Deck(cards=["one", "two", "three", 'four', '5', '6'], name="Test json str")
    d.export("jsON", to_file=True, location="tests/test_str.json")
    e = Deck()
    e.load("tests/test_str.json", is_file=True)
    assert e._cards == d._cards
    assert d._save_location == e.file_location
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_json_import_export_base_card():
    d = Deck(cards=[BaseCard("One"), BaseCard("Two"), BaseCard("Three"), BaseCard("Four")],
             name="Test json basecard")
    d.export("jSon ", to_file=True, location="tests/test_basecard.json")
    e = Deck()
    e.load("tests/test_basecard.json", is_file=True)
    assert e._cards[0].__dict__ == d._cards[0].__dict__
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
def test_json_import_export_custom_card():
    d = Deck(cards=[ExportCard("One"), ExportCard("Two"), ExportCard("Three")], name="Test json custom")
    d.export("   json", to_file=True, location="tests/test_custom.json")
    e = Deck(name="This will get overriden")
    e.load("tests/test_custom.json", is_file=True)
    assert e._cards == d._cards
    assert e._reshuffle == d._reshuffle
    assert e.name == d.name


# noinspection PyProtectedMember,PyProtectedMember
def test_import_standard():
    d = Deck()
    d.load("pyCardDeck/standard_deck.yml", is_file=True)
    e = Deck()
    e.load_standard_deck()
    assert e._cards == d._cards


def test_load_exception():
    d = Deck()
    with pytest.raises(UnknownFormat):
        d.load("")


def test_export_exception():
    d = Deck()
    with pytest.raises(UnknownFormat):
        d.export("")


def test_json():
    d = Deck()
    d.load_standard_deck()
    prop = d.json
    export = d.export("json")
    assert prop == export


def test_yaml():
    d = Deck()
    d.load_standard_deck()
    prop = d.yaml
    export = d.export("yaml")
    assert prop == export
