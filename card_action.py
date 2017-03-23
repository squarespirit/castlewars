from abc import abstractmethod


class CardAction():
    def play(self, you, opponent, is_by_you):
        """
        Carry out the card action.
        :param you: The Player representing you.
        :param opponent: The Player representing your opponent.
        :param is_by_you: True if the card was played by you.
        """
        if is_by_you:
            self._play(you, opponent)
        else:
            self._play(opponent, you)

    @abstractmethod
    def _play(self, player, opponent):
        """
        Carry out the card action.
        :param player: Player who played the card.
        :param opponent: Player's opponent.
        """
        pass


class ResourceChange():
    def __init__(self, resource, amount, is_on_player):
        """
        Construct a resource change.
        :param resource: Resource to be changed.
        :param amount: Integer amount by which to change resource.
        :param is_on_player: True if the change is applied to the player who
            played the card (that caused this resource change).
        """
        self.resource = resource
        self.amount = amount
        self.is_on_player = is_on_player

    def _play(self, player, opponent):
        """Apply the resource change."""
        if self.is_on_player:
            player.change_resource(self.resource, self.amount)
        else:
            opponent.change_resource(self.resource, self.amount)


class ResourceTransfer():
    def __init__(self, resource, amount):
        """
        Construct a resource transfer action in favor of the card player.
        :param resource: Resource to transfer.
        :param amount: Positive integer amount; transfer at most this amount.
        """
        self.resource = resource
        assert self.amount >= 1
        self.amount = amount

    def _play(self, player, opponent):
        """Apply the resource transfer."""
        transfer_amount = min(opponent.resources[self.resource], self.amount)
        # Move 'transfer_amount' stocks from opponent to player
        opponent.change_resource(self.resource, -transfer_amount)
        player.change_resource(self.resource, transfer_amount)


