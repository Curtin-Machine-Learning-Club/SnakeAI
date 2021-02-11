"""
    Author    : Milan Marocchi
    Date      : 10/02/2021
    Purpose   : Contains code for the snake game
    Reference : https://github.com/python-engineer/python-fun/blob/master/snake-pygame/snake_game.py
    NOTE      : All code based off reference and then modified
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class LinearQNet(nn.Module):
    """
    class   : LinearQnet
    purpose : Model for Q learning
    """

    def __init__(self, inputSize, hiddenSize, outputSize):
        """
        Creates an instance of LinearQNet
        :param inputSize: Size of the input layer
        :param hiddenSize: Size of the hidden layer
        :param outputSize: Size of the output layer
        """
        super().__init__()

        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        """
        Returns the output tensors from input tensors
        :return:
        """
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, filename='model.pth'):
        """
        Saves the model onto the computer
        :param filename: The filename of the model to be saved
        """
        modelFolderPath = './model'

        if not os.path.exists(modelFolderPath):
            os.makedirs(modelFolderPath)

        filename = os.path.join(modelFolderPath, filename)
        torch.save(self.state_dict(), filename)


class QTrainer():
    """
    class   : QTrainer
    purpose : Trainer for the Q learning
    """

    def __init__(self, model, lr, gamma):
        """
        Creates an instance of the QTrainer
        :param model: The model being used
        :param lr: The learning rate value
        :param gamma: The gamma value
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)

        self.criterion = nn.MSELoss()

    def trainStep(self, state, finalAction, reward, nextState, done):
        """
        Computes one step of training
        :return:
        """
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        finalAction = torch.tensor(finalAction, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            finalAction = torch.unsqueeze(finalAction, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Get the predicted Q values for the current state
        pred = self.model(state)

        target = pred.clone()
        for index in range(len(done)):
            QNew = reward[index]

            if not done[index]:
                QNew = reward[index] + self.gamma * torch.max(self.model(nextState[index]))

            target[index][torch.argmax(finalAction[index]).item()] = QNew

        # Q-New = Reward + Gamma * max(Next Predicted Q-Value
        # pred.clone()
        # preds[argmax(FinalAction)] = QNew
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
