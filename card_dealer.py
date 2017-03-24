from typing import List, Dict
from card import *
import random


class CardDealer:
    def __init__(self, card_weights: Dict[Card, int]):
        """
        Create a card dealer.
        :param card_weights: card_weights[card] is the relative integer weight
            of that card. card_weights.keys() is the set of all cards.
        """
        self.card_weights = card_weights
        self.total_weight = sum(card_weights.values())

    def deal(self) -> Card:
        """
        Deal a card.
        :return: A card from a weighted random draw.
        """
        rand = random.randrange(self.total_weight)
        for card, weight in self.card_weights.items():
            rand -= weight
            if rand < 0:
                return card
        assert False, 'Didn\'t draw a card at end of deal()'

    def deal_list(self, num_cards: int) -> List[Card]:
        """
        Deal multiple cards.
        :param num_cards: Number of cards.
        :return: A list of cards.
        """
        return [self.deal() for i in range(num_cards)]
