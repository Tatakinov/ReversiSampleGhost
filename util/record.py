#!/usr/bin/python3

import os
import random

import torch
import torch.nn as nn

from agent import Agent
from env import Env
from model import Model

record  = {}
def saveRecord(state, score):
    s   = ''
    for e in state:
        s   += str(e)
    s   += str(score)
    record[s]   = True

model   = Model()

model.load_state_dict(torch.load('model.bin'))
games   = 100
for game in range(games):
    env = Env()
    agent   = Agent(model)
    while not env.isGameOver():
        if env.isPass():
            env.pass_()
            continue
        moves   = env.generateMoves()
        move, score = agent.getBestMove(moves, env)
        state   = env.state()
        saveRecord(state, score)
        env.reverse(move)
    score   = env.finalScore()
    state   = env.state()
    if score > 0:
        saveRecord(state, 1)
    elif score == 0:
        saveRecord(state, 0.5)
    else:
        saveRecord(state, 0)
    print('game{0} was end.'.format(game + 1))

with open('record.txt', mode = 'w') as f:
    for k in record.keys():
        f.write(k)
        f.write('\x0d\x0a')
