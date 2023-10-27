import numpy as np


class Card:
    def __init__(self, surface, seed):
        self.surface = surface
        self.seed = seed

    def __str__(self):
        return "{} {}".format(self.surface, self.seed)

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        if self.surface in {'J', 'Q', 'K'}:
            return 10
        elif self.surface == 'A':
            return 1
        else:
            return int(self.surface)


class BJCard(Card):

    @property
    def value(self):
        if self.surface in {'J', 'Q', 'K'}:
            return 10
        elif self.surface == 'A':
            return 11
        else:
            return int(self.surface)


class Deck:
    def __init__(self, num: int = 1):
        self.cards = []
        for i in range(num):
            self._create_deck()

    def _create_deck(self):
        for surface in ['A', 'J', 'Q', 'K'] + [str(x) for x in range(2, 11)]:
            for seed in ['C', 'H', 'S', 'C']:
                c = BJCard(surface=surface, seed=seed)
                self.cards.append(c)

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal(self, hand_size: int):
        hand = []
        for i in range(hand_size):
            try:
                hand.append(self.cards.pop())
            except IndexError:
                self._create_deck()
                hand.append(self.cards.pop())
        return hand

    @property
    def size(self):
        return len(self.cards)