from abc import abstractmethod


class CardAction():
    def play(self, you, opponent, is_by_you):
        """
        Carry out the card.
        :param you: The Player representing you.
        :param opponent: The Player representing your opponent.
        :param is_by_you: True if the card was played by you.
        :return: True if the card was able to be played.
        """
        if is_by_you:
            return self._play(you, opponent)
        else:
            return self._play(opponent, you)

    @abstractmethod
    def _play(self, player, opponent):
        """
        Carry out the card's cost and actions.
        :param player: Player who played the card.
        :param opponent: Player's opponent.
        :return: True if the player was able to play the card.
            (False if the player couldn't afford it.)
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





