Hearthstone Arena
-----------------

This shows how simple something like drafting can be with pyCardDeck. Although not much more complicated
with just a list :D

.. code-block:: python

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    """
    This is an example of pyCardDeck, it's not meant to be complete poker script,
    but rather a showcase of pyCardDeck's usage.
    """

    import pyCardDeck
    import random
    import requests

    arena_deck = pyCardDeck.Deck(reshuffle=False, name="Awesome arena deck!")
    rarity = {"Common": 100, "Rare": 50, "Epic": 15, "Legendary": 1}


    def card_choice() -> list:
        """
        Picks a rarity, then lets you make a choice

        :return:    List with the card information
        """
        pick_rarity = random.choice([k for k in rarity for _ in range(rarity[k])])
        # This api doesn't provide an easy way to get class and rarity filter at the same time
        # and I'm too lazy to look for another, reminder: this is an example
        cards = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards/qualities/{}".format(pick_rarity),
                             headers={"X-Mashape-Key": "GkQg9DFiZWmshWn6oYqlfXXlXeK9p1QuB6QjsngIi1sHnJiJqv"}).json()
        first, second, third = [random.choice(cards)] * 3
        while second == first:
            second = random.choice(cards)
        while third == first or third == second:
            third = random.choice(cards)
        choice = input("Which one would you like?\n 1: {0}, 2: {1}, 3: {2}\n".format(
            first['name'], second['name'], third['name']))
        while choice not in ["1", "2", "3"]:
            if choice == "1":
                return first
            elif choice == "2":
                return second
            elif choice == "3":
                return third


    def draft():
        """
        Simple draft logic
        """
        for _ in range(30):
            arena_deck.add_single(card_choice())
        print(arena_deck)


    if __name__ == '__main__':
        draft()
