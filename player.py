class Player():
    def __init__(self, resources):
        """
        Construct a new player with starting resources.
        :param resources: Resource -> starting amount dictionary.
        """
        self.resources = resources

    def change_resource(self, resource, amount):
        """
        Change resource by the specified amount. If the player's resource would
        go below 0, cap at 0.
        """
        self.resources[resource] = min(0, self.resources[resource] + amount)