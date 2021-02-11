"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the AI state of the game
"""

from SnakeAI import SnakeAI
from State import State


class AIState(State):
    """
    class   : AIState
    purpose : Contains the code for the AI controlled State
    """

    def __init__(self, game, blockSize):
        """
        Creates an Instance of the AIState
        :param game: A pointer to the game
        :param blockSize: Size of the blocks
        """
        super().__init__(game, blockSize)

    def createSnake(self, width, height, blockSize):
        """
        Creates an AI controlled Snake
        :param width: The width of the window
        :param height: The height of the window
        :param blockSize: The size of the blocks
        :return: A SnakeAI instance
        """
        return SnakeAI(width, height, blockSize)

    def setDirection(self):
        """
        Sets the direction of the SnakeAI
        :param action: Action to occur
        """
        pass

    def moveSnake(self, action):
        """
        Moves the SnakeAI
        :param action: Action to occur
        """
        self.snake.move(action)

    def checkGameOver(self):
        """
        Checks if there is a game over
        :return: returns the game over state
        """
        if self.game.collision() or self.frameIteration > 100 * len(self.snake.getBody()):
            self.gameOver = True

        return self.gameOver

    def processGameOver(self):
        """
        Processes the game over even
        :return: The reward, gameover status and the score
        """
        self.reward = -10
        return self.reward, self.gameOver, self.score

    def getGameOverAndScore(self):
        """
        Returns the game over state and the score
        :return: reward, gameOver and the score
        """
        return self.reward, self.gameOver, self.score

    def processFood(self):
        """
        Processes the food to see if collided with snack (snake)
        """
        if self.snake.getHead() == self.game.food:
            self.score += 1
            self.reward = 10
            self.game._placeFood()
        else:
            self.snake.popBody()

    def resetReward(self):
        """
        Resets the reward to 0
        """
        self.reward = 0

    def reset(self):
        """
        Resets the game state
        """
        # Init snake
        self.snake = self.createSnake(self.game.width, self.game.height, self.BLOCKSIZE)

        # Init state
        self.score = 0
        self.food = None
        self.game._placeFood()
        self.reward = 0

        self.gameOver = False
        self.frameIteration = 0
