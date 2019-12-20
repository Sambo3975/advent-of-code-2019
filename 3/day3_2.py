import numpy as np
import copy


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        """Scalar multiplication"""
        return Point(self.x * other, self.y * other)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __repr__(self):
        return 'Point(%d, %d)' % (self.x, self.y)

    def direction(self):
        return Point(np.sign(self.x), np.sign(self.y))

    def dist(self, other):
        """Manhattan distance"""
        return abs(self.x - other.x) + abs(self.y - other.y)


def vectorize(instruction):
    directions = {
        'R': Point(1, 0),
        'L': Point(-1, 0),
        'U': Point(0, 1),
        'D': Point(0, -1),
    }
    return directions[instruction[0]] * int(instruction[1:])


def get_extents(instructions):
    min_pos = Point()
    max_pos = Point()
    cur_pos = Point()
    for v in instructions:
        cur_pos += v
        min_pos.x = min(min_pos.x, cur_pos.x)
        min_pos.y = min(min_pos.y, cur_pos.y)
        max_pos.x = max(max_pos.x, cur_pos.x)
        max_pos.y = max(max_pos.y, cur_pos.y)
    return min_pos, max_pos


def get_closest_crossing():
    with open('input.txt', 'r') as f:
        wire1_vectors = [vectorize(x) for x in f.readline().split(',')]
        wire2_vectors = [vectorize(x) for x in f.readline().split(',')]
    min_pos, max_pos = get_extents(wire1_vectors)
    board = np.zeros((max_pos.x - min_pos.x + 1, max_pos.y - min_pos.y + 1))
    port = -min_pos
    cur_pos = copy.copy(port)
    for v in wire1_vectors:
        d = v.direction()
        while v.x != 0 or v.y != 0:
            cur_pos += d
            v -= d
            board[cur_pos.x, cur_pos.y] = -1

    cur_pos = copy.copy(port)
    steps = 0
    for v in wire2_vectors:
        d = v.direction()
        while v.x != 0 or v.y != 0:
            cur_pos += d
            v -= d
            steps += 1
            # If we are off of the board, the wires can't possibly cross
            if 0 <= cur_pos.x < board.shape[0] and 0 <= cur_pos.y < board.shape[1] and board[cur_pos.x, cur_pos.y]:
                # Wires cross
                board[cur_pos.x, cur_pos.y] = steps

    cur_pos = copy.copy(port)
    steps = 0
    min_dist = board.shape[0] * board.shape[1]
    for v in wire1_vectors:
        d = v.direction()
        while v.x != 0 or v.y != 0:
            cur_pos += d
            v -= d
            steps += 1
            if board[cur_pos.x, cur_pos.y] > 0:
                min_dist = min(min_dist, board[cur_pos.x, cur_pos.y] + steps)
    return min_dist


if __name__ == '__main__':
    print(get_closest_crossing())
