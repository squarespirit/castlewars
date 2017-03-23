from typing import List
from card_action import *
from player import *

class Card():
    def __init__(self, name: str, cost_resource: str, cost_amount: int,
                 actions: List[CardAction], description: str = None):
        """
        Create a card.
        :param name: Card name.
        :param cost_resource: Resource deducted.
        :param cost_amount: Amount of resource to deduct.
        :param actions: List of CardAction(s) played by this card.
        :param description: Optional description of card actions.
        """
        self.name = name
        self.cost_resource = cost_resource
        self.cost_amount = cost_amount
        assert len(actions) >= 1
        self.actions = actions
        self.description = description

    def play(self, you: Player, opponent: Player, is_by_you: bool):
        """
        Play the card, from your perspective.
        :param you: Player representing you.
        :param opponent: Player representing your opponent.
        :param is_by_you: True if the card was played by you.
        :return: True if the card was successfully played; False if the card
            is not playable.
        """
        if is_by_you:
            self._play(you, opponent)
        else:
            self._play(opponent, you)

    def _play(self, player: Player, opponent: Player):
        """
        Play the card, from the card player's perspective.
        :param player: Player who played the card.
        :param opponent: Player representing their opponent.
        :return: True if the card was successfully played; False if the card
            is not playable.
        """
        # Can't afford
        if player[self.cost_resource] < self.cost_amount:
            return False

        player.lose_resource(self.cost_resource, self.cost_amount)
        for action in self.actions:
            action.do(player, opponent)