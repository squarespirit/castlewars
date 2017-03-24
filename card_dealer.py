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


def read_cards(filename: str) -> CardDealer:
    """
    Read card definitions from a file.
    :param filename: File to read from.
    :return: Card dealer.
    """
    card_weights = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()
            # Ignore blank lines and comments
            if line == '' or line.startswith('#'):
                continue

            # Assume it's card data. Read and strip next 4 lines.
            name = line.title()
            weight = int(next(f).strip())
            cost_line = next(f).strip()
            actions_line = next(f).strip()

            # Parse cost and actions
            cost_resource = cost_line[0]
            cost_amount = int(cost_line[1:])
            actions = []
            # Split actions_line by whitespace
            for action_str in actions_line.split():
                if action_str[:2] == 'at':
                    actions.append(Attack(int(action_str[2:])))
                elif action_str[0] == 't':
                    actions.append(ResourceTransfer(
                        action_str[1], int(action_str[2:])))
                elif action_str[0] == 'o':
                    # Resource change for opponent
                    actions.append(ResourceChange(
                        action_str[1], int(action_str[2:]), False))
                else:
                    # Resource change for player
                    actions.append(ResourceChange(
                        action_str[0], int(action_str[1:]), True))

            description = None
            # Read further lines for @-decorated terms
            while f.read(1) == '@':
                line_split = next(f).strip().split(maxsplit=1)
                if line_split[0] == 'description':
                    description = line_split[1]

            card_weights[Card(name, cost_resource, cost_amount, actions,
                              description)] = weight

    return CardDealer(card_weights)
