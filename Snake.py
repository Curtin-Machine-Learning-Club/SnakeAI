"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake in the snake game
    Reference : https://github.com/python-engineer/python-fun/blob/master/snake-pygame/snake_game.py
    NOTE      : All code based off reference and then modified
"""

from collections import namedtuple
from Direction import Direction

Point = namedtuple('Point', 'x, y')


class Snake:
    """
    class   : Snake
    purpose : Contains the code for a snake in a snake game
    """
    def __init__(self, width, height, blockSize):
        """
        Initialises the snake
        :param width: Width of the window
        :param height: Height of the window
        :param blockSize: Size of each block
        """
        self.BLOCKSIZE = blockSize
        self.direction = Direction.RIGHT
        self.head = Point(width / 2, height / 2)
        self.body = [self.head, Point(self.head.x - self.BLOCKSIZE, self.head.y),
                     Point(self.head.x - (2 * self.BLOCKSIZE), self.head.y)]

    def getBody(self):
        """
        Returns the body of the snake
        :return: Body of the snake
        """
        return self.body

    def setDirection(self, direction):
        """
        Sets the direction of the snake
        :param direction: Direction of the snake to travel
        """
        self.direction = direction

    def getDirection(self):
        """
        Gets the direction of the snake
        :return: The direction of the snake
        """
        return self.direction

    def move(self):
        """
        Moves the snake in the direction it is facing
        """
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

    def insertBody(self):
        """
        Inserts the head into the snakes body to move it
        """
        self.body.insert(0, self.head)

    def getHead(self):
        """
        Gets the head position of the snake
        :return: THe head of the snake
        """
        return self.head

    def popBody(self):
        """
        Removes the lagging parts of the snake
        """
        self.body.pop()