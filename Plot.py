"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake game
    Reference : https://github.com/python-engineer/python-fun/blob/master/snake-pygame/snake_game.py
    NOTE      : All code based off reference and then modified
"""

import matplotlib.pyplot as plt
from IPython import display

class Plot():
    """
    class   : Plot
    purpose : For Plots
    """

    def __init__(self):
        """
        Creates an instance of Plot and set it up
        """
        plt.ion()

    def plot(self, scores, meanScores):
        """
        Plots the scores and mean scores of the model during training
        :param scores: The scores
        :param meanScore: The mean scores
        """
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(scores)
        plt.plot(meanScores)
        plt.ylim(ymin=0)
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
        plt.text(len(meanScores)-1, meanScores[-1], str(meanScores[-1]))
