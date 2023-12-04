#!/usr/bin/python3

def toIndex(x, y):
    return 8 * y + x

def toPos(index):
    x   = index % 8
    y   = index // 8
    return (x, y)

class Env():
    def __init__(self):
        self.color_ = 1
        self.board_ = [ 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0,-1, 1, 0, 0, 0,
                        0, 0, 0, 1,-1, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0]

    def state(self):
        array   = [0] * 128
        for i in range(64):
            if self.board_[i] == self.color_:
                array[2 * i + 0]    = 1
            elif self.board_[i] == -self.color_:
                array[2 * i + 1]    = 1
        return array

    def isGameOver(self):
        p_moves = self.generateMoves()
        self.color_ *= -1
        o_moves = self.generateMoves()
        self.color_ *= -1
        return len(p_moves) + len(o_moves) == 0

    def finalScore(self):
        total   = 0
        for i in range(64):
            total   += self.board_[i]
        return total * self.color_

    def isPass(self):
        return len(self.generateMoves()) == 0

    def pass_(self):
        self.color_ *= -1

    def generateMoves(self):
        moves   = []
        for i in range(64):
            if self.reverse(i, False):
                moves.append(i)
        return moves

    def reverse(self, index, do_reverse = True):
        is_reversible   = self.reverse1(index, False)
        if is_reversible and do_reverse:
            self.reverse1(index, True)
            self.color_ *= -1
        return is_reversible

    def reverse1(self, index, do_reverse):
        if self.board_[index] != 0:
            return
        if do_reverse:
            self.board_[index]  = self.color_

        x, y    = toPos(index)

        reverse = False
        reverse = self.reverse2(x + 1, y    , 0, False, do_reverse) or reverse
        reverse = self.reverse2(x + 1, y + 1, 1, False, do_reverse) or reverse
        reverse = self.reverse2(x    , y + 1, 2, False, do_reverse) or reverse
        reverse = self.reverse2(x - 1, y + 1, 3, False, do_reverse) or reverse
        reverse = self.reverse2(x - 1, y    , 4, False, do_reverse) or reverse
        reverse = self.reverse2(x - 1, y - 1, 5, False, do_reverse) or reverse
        reverse = self.reverse2(x    , y - 1, 6, False, do_reverse) or reverse
        reverse = self.reverse2(x + 1, y - 1, 7, False, do_reverse) or reverse
        return reverse

    def reverse2(self, x, y, direct, is_reversible, do_reverse):
        index   = toIndex(x, y)
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        elif self.board_[index] == self.color_:
            return is_reversible
        elif self.board_[index] == 0:
            return False

        if direct == 0:
            x   += 1
        elif direct == 1:
            x   += 1
            y   += 1
        elif direct == 2:
            y   += 1
        elif direct == 3:
            x   -= 1
            y   += 1
        elif direct == 4:
            x   -= 1
        elif direct == 5:
            x   -= 1
            y   -= 1
        elif direct == 6:
            y   -= 1
        elif direct == 7:
            x   += 1
            y   -= 1

        is_reversible   = self.reverse2(x, y, direct, True, do_reverse)
        if is_reversible and do_reverse:
            self.board_[index]  = self.color_
        return is_reversible

