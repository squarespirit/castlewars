class Player:
    def __init__(self, resources):
        """
        Construct a new player with starting resources.
        :param resources: Resource -> starting amount dictionary. The player
            makes a private copy of the given dictionary.
        """
        self.resources = dict(resources)

    def change_resource(self, resource, amount):
        """
        Gain or lose some of a resource; it won't go below 0.
        :param resource: Resource to change.
        :param amount: Integer amount.
        """
        self.resources[resource] = max(0, self.resources[resource] + amount)

    def lose_resource(self, resource, amount):
        """
        Lose some of a resource; it won't go below 0.
        :param resource: Resource to lose.
        :param amount: Nonnegative integer amount; lose at most this much.
        """
        assert amount >= 0
        self.change_resource(resource, -amount)

    def attacked(self, amount):
        """
        Get attacked by the specified amount. First lose the fence, then
        the castle. Neither will go below 0.
        :param amount: Positive integer attack amount.
        """
        assert amount >= 1
        if self.resources['F'] >= amount:
            self.resources['F'] -= amount
        else:
            amount_left = amount - self.resources['F']
            self.resources['F'] -= amount
            self.lose_resource('C', amount_left)