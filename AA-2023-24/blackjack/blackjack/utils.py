from typing import Callable


def create_simple_deck():
    deck = []
    seeds = 'S C H D'.split()
    values = [str(x) for x in range(2, 8)] + ['A', 'J', 'Q', 'K']
    for value in values:
        for seed in seeds:
            deck.append((value, seed))
    return deck


def create_deck():
    deck = []
    seeds = 'S C H D'.split()
    values = [str(x) for x in range(2, 11)] + ['A', 'J', 'Q', 'K']
    for value in values:
        for seed in seeds:
            deck.append((value, seed))
    return deck


def create_decks(number: int = 1,
                 deck_generator: Callable = create_deck):
    decks = []
    for i in range(number):
        deck = deck_generator()
        decks.extend(deck)
    return decks


def as_str(card):
    return "{}{}".format(card[0], card[1].lower())