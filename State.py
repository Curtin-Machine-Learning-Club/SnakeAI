"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the Base state for the snake game
"""


class State():
    """
    class   : State
    purpose : A Base class for one of the two states, AI or Player.
    """

    def __init__(self, game, blockSize):
        """
        Creates an instance of State (Only called by children)
        :param game: A pointer to the game object
        :param blockSize: Size of the pixels
        """
        self.game = game
        self.BLOCKSIZE = blockSize

    def processFood(self):
        """
        Processes the food to see if collided with snack (snake)
        """
        if self.snake.getHead() == self.game.food:
            self.score += 1
            self.game._placeFood()
        else:
            self.snake.popBody()

