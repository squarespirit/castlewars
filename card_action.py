from abc import abstractmethod
from resource import *


class CardAction:
    @abstractmethod
    def do(self, player, opponent):
        """
        Do the card action, from the perspective of the card player.
        :param player: Player who played the card.
        :param opponent: Their opponent.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        :return: A string representing the card action. Words, including
            the first word, should be lowercase."""
        pass


class ResourceChange(CardAction):
    def __init__(self, resource, amount, is_for_player):
        """
        Construct a resource change.
        :param resource: Resource to be changed.
        :param amount: Integer amount by which to change resource.
        :param is_for_player: True if the change is applied to the player.
            (False if the change is applied to the opponent.)
        """
        self.resource = resource
        self.amount = amount
        self.is_for_player = is_for_player

    def do(self, player, opponent):
        """Do the resource change."""
        if self.is_for_player:
            player.change_resource(self.resource, self.amount)
        else:
            opponent.change_resource(self.resource, self.amount)

    def __str__(self):
        if self.is_for_player:
            return '{} {:+d}'.format(resource_long[self.resource], self.amount)
        else:
            return 'enemy {} {:+d}'.format(
                resource_long[self.resource], self.amount)


class ResourceTransfer(CardAction):
    def __init__(self, resource, amount):
        """
        Construct a resource transfer action in favor of the card player.
        :param resource: Resource to transfer.
        :param amount: Positive integer amount; transfer at most this amount.
        """
        self.resource = resource
        assert self.amount >= 1
        self.amount = amount

    def do(self, player, opponent):
        """Transfer the resource."""
        transfer_amount = min(opponent.resources[self.resource], self.amount)
        # Move 'transfer_amount' stocks from opponent to player
        opponent.change_resource(self.resource, -transfer_amount)
        player.change_resource(self.resource, transfer_amount)

    def __str__(self):
        return 'transfer {} {}'.format(
            resource_long[self.resource], self.amount)


class Attack(CardAction):
    def __init__(self, amount):
        """
        Construct an attack action.
        :param amount: Positive integer amount to attack.
        """
        assert self.amount >= 1
        self.amount = amount

    def do(self, player, opponent):
        """Do the attack."""
        opponent.attacked(self.amount)

    def __str__(self):
        return 'attack {}'.format(self.amount)