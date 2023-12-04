#!/usr/bin/python3

import os
import torch
import torch.nn as nn

from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

from model import Model

def save(array, f):
    for e in array:
        if type(e) == list:
            save(e, f)
        else:
            f.write(str(e))
            f.write('\x0d\x0a')

def load(f):
    pos = []
    for i in range(64 * 2):
        n   = f.read(1)
        if n == '':
            return (False, False)
        pos.append(int(n))
    value   = float(f.readline())
    return (pos, value)

def main():
    model   = Model()

    if os.path.exists('model.bin'):
        model.load_state_dict(torch.load('model.bin'))
    else:
        torch.save(model.state_dict(), 'model.bin')

    if not os.path.exists('model.txt'):
        with open('model.txt', mode = 'w') as f:
            save(model.layer1.weight.data.tolist(), f)
            save(model.layer1.bias.data.tolist(), f)
            save(model.layer2.weight.data.tolist(), f)
            save(model.layer2.bias.data.tolist(), f)
            save(model.layer3.weight.data.tolist(), f)
            save(model.layer3.bias.data.tolist(), f)

    x_list  = []
    y_list  = []

    with open('record.txt', mode = 'r') as f:
        while True:
            pos, value  = load(f)
            if pos == False:
                break
            x_list.append(pos)
            y_list.append([value])

    x_tensor    = torch.tensor(x_list, dtype=torch.float32)
    y_tensor    = torch.tensor(y_list, dtype=torch.float32)

    dataset = TensorDataset(x_tensor, y_tensor)

    batch_size  = 256
    train_loader    = DataLoader(dataset, batch_size, shuffle = True)

    criterion   = nn.MSELoss(reduction = 'sum')
    optimizer   = torch.optim.Adam(model.parameters(), lr = 0.001)

    epoch_max   = 100
    for epoch in range(epoch_max):
        for x, y in train_loader:
            optimizer.zero_grad()
            predict = model(x)
            loss    = criterion(predict, y)
            loss.backward()
            optimizer.step()
        print('epoc: ', epoch + 1, ' loss: ', loss.item())

    torch.save(model.state_dict(), 'model.bin')

    with open('model.txt', mode = 'w') as f:
        save(model.layer1.weight.data.tolist(), f)
        save(model.layer1.bias.data.tolist(), f)
        save(model.layer2.weight.data.tolist(), f)
        save(model.layer2.bias.data.tolist(), f)
        save(model.layer3.weight.data.tolist(), f)
        save(model.layer3.bias.data.tolist(), f)

main()
