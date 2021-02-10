"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake ai in the snake game
"""

from collections import namedtuple
from Direction import Direction
from Snake import Snake
import numpy as np

Point = namedtuple('Point', 'x, y')


class SnakeAI(Snake):
    def __init__(self, width, height, blockSize):
        super().__init__(width, height, blockSize)

    def move(self, action):
        """
        Moves the snake in the direction it is facing
        """
        # [straight, right, left]

        clockWise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clockWise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            # No Change
            newDirection = clockWise[index]
        elif np.array_equal(action, [0, 1, 0]):
            # Right turn
            nextIndex = (index + 1) % 4
            newDirection = clockWise[nextIndex]
        else:
            # Left turn
            nextIndex = (index - 1) % 4
            newDirection = clockWise[nextIndex]

        self.direction = newDirection

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += self.BLOCKSIZE

        elif self.direction == Direction.LEFT:
            x -= self.BLOCKSIZE

        elif self.direction == Direction.UP:
            y -= self.BLOCKSIZE

        elif self.direction == Direction.DOWN:
            y += self.BLOCKSIZE

        self.head = Point(x, y)
