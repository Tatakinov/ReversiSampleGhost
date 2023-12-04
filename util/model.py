#!/usr/bin/python3

import torch
import torch.nn as nn

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.relu   = nn.LeakyReLU(0.01)
        self.sigmoid    = nn.Sigmoid()
        self.layer1 = nn.Linear(128, 128)
        self.layer2 = nn.Linear(128, 64)
        self.layer3 = nn.Linear(64, 1)

    def forward(self, x):
        x   = self.layer1(x)
        x   = self.relu(x)
        x   = self.layer2(x)
        x   = self.relu(x)
        x   = self.layer3(x)
        x   = self.sigmoid(x)
        return x

