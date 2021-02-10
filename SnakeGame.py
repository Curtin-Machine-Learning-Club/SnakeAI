"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake game
    Reference : https://github.com/python-engineer/python-fun/blob/master/snake-pygame/snake_game.py
    NOTE      : All code based off reference and then modified
"""

import pygame as pyg
from StateFactory import StateFactory
from Direction import Direction
import random
from collections import namedtuple

# Inital Constant Setup
pyg.init()
font = pyg.font.Font('arial.ttf', 25)
Point = namedtuple('Point', 'x, y')

BLACK = (0, 0, 0)
ORANGE = (255, 140, 00)
GREEN1 = (00, 255, 00)
GREEN2 = (0, 128, 0)
SEAFOAMGREEN = (160, 200, 180)

BLOCKSIZE = 20
SPEED = 20


class SnakeGame:
    """
    class   : SnakeGame
    purpose : Contains functionality for a game of snake
    """

    def __init__(self, width=640, height=640, ai=False):
        """
        Init
        :param width: width of the screen
        :param height: height of the screen
        """
        # Set up size
        self.width = width
        self.height = height
        self.state = StateFactory(ai, self, BLOCKSIZE).makeState()

        # Initialise display
        self.display = pyg.display.set_mode((self.width, self.height))
        pyg.display.set_caption("Snack")
        self.clock = pyg.time.Clock()

        # Init snake and state
        self.food = None
        self.state.reset()

        # Init user input
        self.ui = UserInputFactory(ai).makeUserInput()

    def _placeFood(self):
        """
        Places a piece of food in the game
        """
        x = random.randint(0, (self.width - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.width - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE

        self.food = Point(x, y)

        if self.food in self.state.snake.getBody():
            self._placeFood()

    def playStep(self, action=None):
        """
        Plays one step of the game
        :return: Returns the game over status as well as the score
        """
        # Increment frame iteration
        self.state.frameIteration += 1

        # If ai controlled no user input hence just passes
        self.state.setDirection()

        # Move the Snake
        self.state.moveSnake(action)
        self.state.snake.insertBody()

        # Check for game over
        if self.state.checkGameOver():
            self.state.processGameOver()

        # Place more food or move
        self.state.processFood()

        # Update UI and clock
        self._updateUI()
        self.clock.tick(SPEED)

        # Return game over and score
        return self.state.getGameOverAndScore()

    def collision(self, point=None):
        """
        Checks to see if the snake has collided
        :return: Returns true if collision occured
        """
        if point == None:
            point = self.state.snake.getHead()

        output = False
        snakeBody = self.state.snake.getBody()

        if point.x > self.width - BLOCKSIZE or point.x < 0 or point.y > self.height - BLOCKSIZE or point.y < 0:
            output = True
        if point in snakeBody[1:]:
            output = True

        return output

    def _updateUI(self):
        """
        Updates the display, drawing everything to it
        """
        snakeBody = self.state.snake.getBody()

        # Reset display
        self.display.fill(SEAFOAMGREEN)

        # Draw snake
        for pt in snakeBody:
            pyg.draw.rect(self.display, GREEN2, pyg.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
            pyg.draw.rect(self.display, GREEN1, pyg.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw food
        pyg.draw.rect(self.display, ORANGE, pyg.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        # Draw Score
        text = font.render("Score: " + str(self.state.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pyg.display.flip()

    def reset(self):
        """
        Resets the game state
        """
        self.state.reset()


class UserInput():
    """
    class   : UserInput
    Purpose : Takes user input from the player for the game
    """

    def __init__(self):
        """
        Creates an instance of UserInput
        """
        pass

    def getInput(self):
        """
        Gets the key pressed by the user or closes the game if the quit button is
        selected
        :return: The key pressed or None
        """
        keyPressed = None

        for event in pyg.event.get():

            ## Quit if a quit event
            if event.type == pyg.QUIT:
                pyg.quit()
                quit()

            ## Other wise take user input and return
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_LEFT:
                    keyPressed = Direction.LEFT

                elif event.key == pyg.K_RIGHT:
                    keyPressed = Direction.RIGHT

                elif event.key == pyg.K_UP:
                    keyPressed = Direction.UP

                elif event.key == pyg.K_DOWN:
                    keyPressed = Direction.DOWN

        return keyPressed


class AIInput():
    """
    class   : AIInput
    Purpose : Takes user input from the AI for the game
    """

    def __init__(self):
        """
        Creates an instance of UserInput
        """
        pass

    def getInput(self):
        """
        Gets the key pressed by the user or closes the game if the quit button is
        selected
        :return: The key pressed or None
        """
        for event in pyg.event.get():

            ## Quit if a quit event
            if event.type == pyg.QUIT:
                pyg.quit()
                quit()


class UserInputFactory():
    """
    class   : UserInputFactory
    purpose : To Create A user input depending on if it is ai controlled or human controlled
    """
    def __init__(self, ai):
        """
        Creates an instance of the factory
        :param ai: Boolean value, true if ai controlled
        """
        self.ai = ai

    def makeUserInput(self):
        """
        Retruns the proper user input class
        :return: The user input method to be used
        """
        ui = None

        if self.ai == True:
            ui = AIInput()
        else:
            ui = UserInput()

        return ui

def playGame():
    """
    Runs the snake game
    """

    # Create the game
    game = SnakeGame()

    # Run the game loop
    while True:
        gameOver, score = game.playStep()

        if gameOver == True:
            break

    print('Final Score ' + str(score))

    pyg.quit()

if __name__ == "__main__":
    playGame()