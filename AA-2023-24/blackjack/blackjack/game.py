from typing import List

from blackjack.deck import Deck
import numpy as np
import abc


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.hand_value = 0
        self.in_game = True

    def reset(self):
        self.hand = []
        self.hand_value = 0

    def compute_value(self):
        self.hand_value = sum(card.value for card in self.hand)

    def hit(self, deck: Deck):
        self.hand.extend(deck.deal(num=1))
        self.compute_value()

    def stay(self):
        self.in_game = False

    @abc.abstractmethod
    def play(self, deck: Deck):
        pass


class Dealer(Player):
    def play(self, deck: Deck):
        if self.hand_value <= 16:
            self.hit(deck)
        elif 16 < self.hand_value <= 21:
            self.stay()
        else:
            self.in_game = False


class HumanPlayer(Player):
    def __init__(self, name: str, capital: float,
                 bet_rate: float = 2.00):
        super().__init__(name)
        self.capital = capital
        self.bet_rate = bet_rate
        self.history = [self.capital]

    def play(self, deck: Deck):
        if self.hand_value <= 20:
            action = input('{}: {} - hit or stay'.format(
                self.name,
                self.hand_value
            ))
            if action == 'hit':
                self.hit(deck)
            else:
                self.stay()
        elif self.hand_value == 21:
            self.stay()
        else:
            self.in_game = False

    def bet(self, money: float = None):
        if money is None:
            money = self.bet_rate
        self.capital -= money
        return money


class DummyRandomPlayer(HumanPlayer):
    def play(self, deck:Deck):
        if self.hand_value <= 21:
            if np.random.uniform(0, 1) > .5:
                self.hit(deck)
            else:
                self.stay()
        else:
            self.in_game = False


class Table:
    def __init__(self):
        self.deck = Deck.create_basic_deck()
        self.deck.shuffle()
        self.players = []
        self.dealer = Dealer(name='Dealer')
        self.bets = {}
        self.capital = 0
        self.history = [self.capital]

    def add_player(self, player: HumanPlayer):
        self.players.append(player)

    def add_players(self, players: List[HumanPlayer]):
        self.players.extend(players)

    def receive_bets(self, money: List[float] = None):
        if money is None:
            for player in self.players:
                player_bet = player.bet()
                self.bets[player.name] = player_bet
                self.capital += player_bet
        else:
            for i, m in enumerate(money):
                p = self.players[i]
                player_bet = p.bet(money=m)
                self.bets[p.name] = player_bet
                self.capital += player_bet

    def serve_players(self):
        for player in self.players:
            player.hand.extend(self.deck.deal(num=2))
            player.compute_value()
        self.dealer.hand.extend(self.deck.deal(num=2))
        self.dealer.compute_value()

    def play(self):
        for player in self.players:
            while player.in_game:
                player.play(self.deck)
        while self.dealer.in_game:
            self.dealer.play(self.deck)

    def pay(self):
        for player in self.players:
            if player.hand_value <= 21:
                if self.dealer.hand_value > 21:
                    payment = self.bets[player.name] * 2
                    player.capital += payment
                    self.capital -= payment
                else:
                    if player.hand_value > self.dealer.hand_value:
                        payment = self.bets[player.name] * 2
                        player.capital += payment
                        self.capital -= payment
                    elif player.hand_value == self.dealer.hand_value:
                        payment = self.bets[player.name]
                        player.capital += payment
                        self.capital -= payment
                    else:
                        pass
            else:
                pass
            player.reset()
            player.history.append(player.capital)
        self.dealer.reset()
        self.history.append(self.capital)
        self.bets = {}

    def print_player_status(self, print_dealer: bool = False):
        for p in self.players:
            print(p.name, p.hand_value, p.in_game, p.capital, p.hand)
        if print_dealer:
            print(self.dealer.name, self.dealer.hand_value, self.dealer.in_game, self.dealer.hand)

