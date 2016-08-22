from pyCardDeck import *

def test_BaseCard():
    card = BaseCard("BaseCard")
    assert str(card) == "BaseCard"
    assert repr(card) == "BaseCard({'name': 'BaseCard'})"

def test_PokerCard():
    card = PokerCard("Hearts", "J", "Jack")
    assert str(card) == "Jack of Hearts"
    assert card.rank == "J"
    assert repr(card).startswith("PokerCard({'")