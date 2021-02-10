"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the state factory for the snake game
"""

from PlayerState import PlayerState
from AIState import AIState


class StateFactory():
    """
    class   : StateFactory
    purpose : Creates the state depending on what is passed
    """

    def __init__(self, ai, game, blockSize):
        """
        Creates an instance of StateFactory
        :param ai: Boolean, true if AI controlled
        :param game: A pointer to the game object
        :param blockSize: The size of the pixels
        """
        self.ai = ai
        self.game = game
        self.blockSize = blockSize

    def makeState(self):
        """
        Returns the proper state
        :return: Returns the state object to be used
        """
        state = None

        if self.ai == True:
            state = AIState(self.game, self.blockSize)
        else:
            state = PlayerState(self.game, self.blockSize)

        return state
