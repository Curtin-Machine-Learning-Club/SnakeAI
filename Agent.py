"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake game agent
    Reference : https://github.com/python-engineer/snake-ai-pytorch
    NOTE      : All code based off reference
"""

import torch
import random
import numpy as np
import sys
import os
from collections import deque
from SnakeGame import SnakeGame, Point
from Direction import Direction
from Model import LinearQNet, QTrainer
from Plot import Plot

MAXMEMORY = 100_000
BATCHSIZE = 1000
LR = 0.001

class Agent:
    """
    class   : Agent
    purpose : The Agent for the snake game
    """

    def __init__(self):
        """
        Creates an instance of Agent and initializes it
        """
        self.games = 0

        self.epsilon = 0 # randomness
        self.gamma = 0   # discount rate

        self.memory = deque(maxlen=MAXMEMORY)
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # TODO: model and trainer


    def getState(self, game):
        """
        Gets the state from the game
        :param game: A pointer to the game object
        """
        head = game.state.snake.getHead()
        pointLeft = Point(head.x - 20, head.y)
        pointRight = Point(head.x + 20, head.y)
        pointUp = Point(head.x, head.y - 20)
        pointDown = Point(head.x, head.y + 20)

        dirLeft = game.state.snake.getDirection() == Direction.LEFT
        dirRight = game.state.snake.getDirection() == Direction.RIGHT
        dirUp = game.state.snake.getDirection() == Direction.UP
        dirDown = game.state.snake.getDirection() == Direction.DOWN

        state = [
            # Danger Straight
            (dirRight and game.collision(pointRight)) or
            (dirLeft and game.collision(pointLeft)) or
            (dirUp and game.collision(pointUp)) or
            (dirDown and game.collision(pointDown)),

            # Danger Right
            (dirUp and game.collision(pointRight)) or
            (dirDown and game.collision(pointLeft)) or
            (dirLeft and game.collision(pointUp)) or
            (dirRight and game.collision(pointDown)),

            # Danger Left
            (dirDown and game.collision(pointRight)) or
            (dirUp and game.collision(pointLeft)) or
            (dirRight and game.collision(pointUp)) or
            (dirLeft and game.collision(pointDown)),

            # Move Direction
            dirLeft,
            dirRight,
            dirUp,
            dirDown,

            # Food Location
            game.food.x < game.state.snake.head.x,  # food left
            game.food.x > game.state.snake.head.x,  # food right
            game.food.y < game.state.snake.head.y,  # food up
            game.food.y > game.state.snake.head.y  # food down
        ]

        return state


    def remember(self, state, action, reward, nextState, done):
        """
        Adds state action reward nextState and done to the memory
        :param state: The state of the game
        :param action: The action chose
        :param reward: The reward for the action
        :param nextState: The next state
        :param done: If the game has finished
        """
        # Pops left if memory limit is reached (hence forgets old memory)
        self.memory.append((state, action, reward, nextState, done))

    def trainLongMemory(self):
        """
        Uses the trainer to train the long memory
        """
        if len(self.memory) > BATCHSIZE:
            miniSample = random.sample(self.memory, BATCHSIZE)
        else:
            miniSample = self.memory

        # Take all the data from the miniSample
        states, actions, rewards, nextStates, dones = zip(*miniSample)

        self.trainer.trainStep(states, actions, rewards, nextStates, dones)


    def trainShortMemory(self, state, action, reward, nextState, done):
        """
        Uses the trainer to train the short memory
        :param state: The current state of the game
        :param action: The action performed
        :param reward: The reward for the action
        :param nextState: The next state of the game
        :param done: If the game is finished
        """
        self.trainer.trainStep(state, action, reward, nextState, done)

    def getAction(self, state):
        """
        Determines the action for the agent to perform
        :param state: The current state of the game
        """
        # Random moves: tradeoff exploration and exploitation
        self.epsilon = 80 - self.games
        finalAction = [0,0,0]

        if random.randint(0, 200) < self.epsilon:
            action = random.randint(0, 2)
            finalAction[action] = 1
        else:
            finalAction = self.getTrainedAction(state)

        return finalAction

    def getTrainedAction(self, state):
        """
        Determins the action for the agent to perform (Only uses trained actions) 
        :param state: The current state of the game
        """

        finalAction = [0, 0, 0]
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.model(state0)
        action = torch.argmax(prediction).item()
        finalAction[action] = 1
        
        return finalAction

    def loadModel(self, filename='model.pth'):
        """
        Loads a model from a file
        :param filename: The filename of the model file
        """
        modelFolderPath = './model'
        filename = os.path.join(modelFolderPath, filename)

        self.model.load_state_dict(torch.load(filename))
        self.model.eval()


def train():
    """
    Trains the model using the agent and the game
    """
    # For Plots
    plot = Plot()
    plotScores = list()
    plotMeanScores = list()
    totalScore = 0
    meanScore = 0

    highestScore = 0
    agent = Agent()
    game = SnakeGame(ai=True)

    while True:
        # Get old/current state
        stateOld = agent.getState(game)

        # Get move based on current state
        finalAction = agent.getAction(stateOld)

        # Perform the move and get next state
        reward, done, score = game.playStep(finalAction)
        stateNew = agent.getState(game)

        # Train short memory
        agent.trainShortMemory(stateOld, finalAction, reward, stateNew, done)

        # Remember (to store in the memory)
        agent.remember(stateOld, finalAction, reward, stateNew, done)

        if done:
            # Train long memory
            game.reset()
            agent.games += 1
            agent.trainLongMemory()

            if score > highestScore:
                highestScore = score
                agent.model.save()

            print('Game', agent.games, 'Score', score, 'High Score:', highestScore)

            plotScores.append(score)
            totalScore += score
            meanScore = totalScore / agent.games
            plotMeanScores.append(meanScore)
            plot.plot(plotScores, plotMeanScores)

def run():
    """
    Runs the model without training it
    """
    
    highestScore = 0
    agent = Agent()
    agent.loadModel()
    game = SnakeGame(ai=True)
    done = False    

    while not done:
        stateOld = agent.getState(game)

        finalAction = agent.getTrainedAction(stateOld)

        reward, done, score = game.playStep(finalAction)
        stateNew = agent.getState(game)
    
    print("Score was:", score)


if __name__ == "__main__":
    usage = "Invalid Usage: python3 Agent.py <run/train>"

    if len(sys.argv) != 2:
        print(usage)
    else:
        if sys.argv[1] == "run":
            run()
        elif sys.argv[1] == "train":
            train()
        else:
            print(usage)
