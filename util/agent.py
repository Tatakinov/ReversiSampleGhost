#!/usr/bin/python3

import copy
import random

import torch

depth   = 0

def tensor(state):
    return torch.tensor(state, dtype=torch.float32)

class Agent():
    def __init__(self, model):
        self.model_ = model
        pass

    def negaalpha(self, env, depth, alpha, beta):
        if env.isGameOver():
            s   = env.finalScore()
            if s > 0:
                return 1
            elif s < 0:
                return 0
            else:
                return 0.5

        if depth <= 0:
            return self.model_(tensor(env.state())).item()

        if env.isPass():
            e   = copy.deepcopy(env)
            e.pass_()
            return 1 - self.negaalpha(
                    e, depth - 1, 1 - beta, 1 - alpha
                    )

        score   = -1
        for m in env.generateMoves():
            e   = copy.deepcopy(env)
            e.reverse(m)
            s   = 1 - self.negaalpha(
                    e, depth - 1, 1 - beta, 1 - max(alpha, score)
                    )
            if s > score:
                score   = s
                if score >= beta:
                    break
        return score

    def getBestMove(self, moves, env):
        move    = None
        score   = -1
        scores  = []
        random_choice_factor    = []
        for m in moves:
            e   = copy.deepcopy(env)
            e.reverse(m)
            s   = 1 - self.negaalpha(e, depth, -0.001, 1.001)
            scores.append(s)
            if s > score:
                move    = m
                score   = s
        total   = 0
        for s in scores:
            factor  = s * s
            factor  = factor * factor
            factor  = factor * factor
            factor  = factor * factor
            random_choice_factor.append(factor)
            total   += factor
        if total > 0:
            for i in range(len(random_choice_factor)):
                random_choice_factor[i] /= total
        r   = random.random()
        for i in range(len(random_choice_factor)):
            r   -= random_choice_factor[i]
            if r < 0:
                return (moves[i], score)
        return (move, score)
