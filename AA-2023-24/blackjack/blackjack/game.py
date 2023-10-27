def blackjack_card_value(card):
    surface = card[0]
    if surface in {'J', 'K', 'Q'}:
        return 10
    elif surface == 'A':
        return 11
    else:
        return int(surface)