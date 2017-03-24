from card import *


class PlayerTurn:
    """Represents what a player did on their turn."""
    pass


class CardTurn(PlayerTurn):
    """Represents that a player played a card on their turn."""

    def __init__(self, card: Card):
        """
        :param card: Card that was played.
        """
        self.card = card


class DiscardTurn(PlayerTurn):
    """Represents that a player discarded some cards on their turn."""

    def __init__(self, discards: Card):
        """
        :param discards: List of discarded cards.
        """
        self.discards = discards