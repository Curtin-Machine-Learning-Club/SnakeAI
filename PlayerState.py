"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the player controlled state of the snake game
"""

from Snake import Snake
from State import State


class PlayerState(State):
    """
    class   : PlayerState
    purpose : Contains the implementation for the player controlled state
    """

    def __init__(self, game, blockSize):
        """
        Creates an Instance of PlayerState
        :param game: A pointer to the game class
        :param blockSize: The size of the blocks
        """
        super().__init__(game, blockSize)

    def createSnake(self, width, height, blockSize):
        """
        Creates a Player Controlled Snake
        :param width: The width of the window
        :param height: The height of the window
        :param blockSize: The size of the blocks
        :return: An instance of Snake
        """
        return Snake(width, height, blockSize)

    def setDirection(self):
        """
        Sets the direction of the snake
        :param action: None
        """
        # User Input
        inputKey = self.game.ui.getInput()
        if inputKey != None:
            self.snake.setDirection(inputKey)

    def moveSnake(self, action):
        """
        Moves the snake
        :param action: None
        """
        self.snake.move()

    def checkGameOver(self):
        """
        Checks for game over
        :return: Game Over state
        """
        if self.game.collision():
            self.gameOver = True

        return self.gameOver

    def processGameOver(self):
        """
        Returns the Game Over returns
        :return: GameOver state and score
        """
        return self.gameOver, self.score

    def getGameOverAndScore(self):
        """
        Returns the game over state and the score
        :return: gameOver and the score
        """
        return self.gameOver, self.score

    def resetReward(self):
        """
        Does nothing, only for the AI State
        """
        pass

    def reset(self):
        """
        Resets the game state
        """
        # Init snake
        self.snake = self.createSnake(self.game.width, self.game.height, self.BLOCKSIZE)

        # Init state
        self.score = 0
        self.game._placeFood()

        self.gameOver = False
        self.frameIteration = 0
