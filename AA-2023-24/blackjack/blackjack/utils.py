
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


def create_decks(number: int = 1, deck_generator = create_deck):
    decks = []
    for i in range(number):
        deck = deck_generator()
        decks.extend(deck)
    return decks

