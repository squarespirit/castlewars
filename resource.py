from enum import Enum

class Resource(str):
    def __init__(self, char):
        """
        Construct a new Resource as a one-character string.
        :param char:
        """
        assert len(char) == 1
        super(char)

