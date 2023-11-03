from typing import List, Any

import blackjack.utils as ut
import blackjack.game as gm
import numpy as np


BLACKJACK_VALUES = {
    'A': 11,
    'J': 10,
    'Q': 10,
    'K': 10
}


def value_card(card: ut.Card) -> int:
    if card.symbol in BLACKJACK_VALUES.keys():
        return BLACKJACK_VALUES[card.symbol]
    else:
        try:
            return int(card.symbol)
        except ValueError:
            raise ValueError('{} is not a valid card value'.format(card.symbol))


class BJCard(ut.Card):

    @property
    def value(self):
        return value_card(self)

    def __str__(self):
        return "{}|{}".format(self.symbol, self.seed)

    def __repr__(self):
        return self.__str__()


class Deck:

    def __init__(self, num: int = 1):
        self.deck = []
        self.number_of_base_decks = num
        self._create_deck(num=self.number_of_base_decks)

    def _create_deck(self, num: int = 1):
        symbols = [str(x) for x in range(2, 11)] + ['A', 'J', 'Q', 'K']
        self.deck = [
            BJCard(x.symbol, x.seed) for x in
            ut.create_decks(symbols=symbols, num=num)]

    @classmethod
    def create_basic_deck(cls):
        deck = cls(num=1)
        return deck

    def shuffle(self):
        np.random.shuffle(self.deck)

    @property
    def size(self):
        return len(self.deck)

    def deal(self, num: int = 1) -> List[ut.Card]:
        hand = []
        for i in range(num):
            try:
                hand.append(self.deck.pop())
            except IndexError:
                self._create_deck(num=self.number_of_base_decks)
                self.shuffle()
                hand.append(self.deck.pop())
        return hand

