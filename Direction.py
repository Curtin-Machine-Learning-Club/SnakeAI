"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code a direction Enum
    Reference : https://github.com/python-engineer/python-fun/blob/master/snake-pygame/snake_game.py
    NOTE      : All code based off reference and then modified
"""

from enum import Enum


class Direction(Enum):
    """
    Enum for Directions
    """
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
