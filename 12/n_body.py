from copy import deepcopy
from multiprocessing.pool import Pool
from re import findall

from math import gcd


class V3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return '<x=%d, y=%d, z=%d>' % (self.x, self.y, self.z)

    def __add__(self, other):
        return V3(self.x + other.x, self.y + other.y, self.z + other.z)

    def manhattan(self):
        """Get the Manhattan distance represented by the vector"""
        return abs(self.x) + abs(self.y) + abs(self.z)


def sign(val):
    if val == 0:
        return 0
    return -1 if val < 0 else 1


class Satellite:
    def __init__(self, px, py, pz):
        self.pos = V3(px, py, pz)
        self.vel = V3()

    def __repr__(self):
        return 'pos=%s, vel=%s' % (repr(self.pos), repr(self.vel))

    def update_vel(self, others):
        for s in others:
            self.vel.x += sign(s.pos.x - self.pos.x)
            self.vel.y += sign(s.pos.y - self.pos.y)
            self.vel.z += sign(s.pos.z - self.pos.z)

    def update_pos(self):
        self.pos += self.vel

    def get_total_energy(self):
        return self.pos.manhattan() * self.vel.manhattan()


class Satellite1D:
    def __init__(self, p):
        self.pos = p
        self.vel = 0

    def update_vel(self, others):
        for s in others:
            self.vel += sign(s.pos - self.pos)

    def update_pos(self):
        self.pos += self.vel


def load_body_data(filename, split_by_dimension=False):
    if split_by_dimension:
        data = [[], [], []]
    else:
        data = []
    with open(filename, 'r') as f:
        # a line has the format '<x=V, y=V, z=V>', where V is any number of digits possibly preceded by a '-'
        for line in f.readlines():
            e = [int(x) for x in findall(r'-?\d+', line)]
            if split_by_dimension:
                for i in range(3):
                    data[i].append(Satellite1D(e[i]))
            else:
                data.append(Satellite(e[0], e[1], e[2]))
    return data


def get_total_system_energy(data):
    total = 0
    for s in data:
        total += s.get_total_energy()
    return total


def simulate_motion(data, steps=1000):
    for i in range(steps):
        for s in data:
            s.update_vel(data)
        for s in data:
            s.update_pos()
    return get_total_system_energy(data)


def check_cycle_reached(data, initial_data):
    for current, initial in zip(data, initial_data):
        if current.vel != initial.vel or current.pos != initial.pos:
            return False
    return True


def get_1d_cycle_length(data):
    initial_data = deepcopy(data)
    steps = 0
    while steps == 0 or not check_cycle_reached(data, initial_data):
        for s in data:
            s.update_vel(data)
        for s in data:
            s.update_pos()
        steps += 1
    print(steps)
    return steps


def get_3d_cycle_length(data):
    # The way this problem is set up makes the motion in one dimension independent from the motion in the others.
    # Thus, the length of a full cycle is the lcm of the lengths of a cycle in each dimension. Using this fact, I can
    # drastically reduce the number of operations by computing the cycle length for each dimension individually.
    p = Pool(3)  # I will reduce computation time further by using multiprocessing
    cycle_lengths = p.map(get_1d_cycle_length, data)
    lcm = cycle_lengths[0]
    for i in cycle_lengths[1:]:
        lcm *= i // gcd(lcm, i)
    return lcm


if __name__ == '__main__':
    # Part 1
    body_data = load_body_data('data.txt')
    system_energy = simulate_motion(body_data)
    print('Total system energy after 1000 steps:')
    print(system_energy)
    # Part 2
    body_data_split = load_body_data('data.txt', True)
    print('Cycle lengths in each dimension:')
    cycle_length = get_3d_cycle_length(body_data_split)
    print('Total cycle length:')
    print(cycle_length)

