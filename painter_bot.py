from numpy import insert
from numpy.ma import array

from intcode import IntcodeComputer

paint_print_map = {
    -2: '+',  # black (unpainted, start zone)
    -1: '-',  # black (unpainted, tiles start black)
    0:  '.',  # black (painted)
    1:  '#',  # white (painted)
}

robot_print_map = {
    repr([0, -1]): '^',  # up
    repr([0, 1]):  'v',  # down
    repr([-1, 0]): '<',  # left
    repr([1, 0]):  '>',  # right
}


class PainterBot:
    def __init__(self):
        self.brain = IntcodeComputer()
        self.brain.load('painter')
        self.position = [1, 1]
        self.direction = [0, -1]
        self.map = array([[-2, -2, -2], [-2, -2, -2], [-2, -2, -2]])

    def __repr__(self):
        print_string = 'PainterRobot:\n'
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if x == self.position[0] and y == self.position[1]:
                    print_string += robot_print_map[repr(self.direction)]
                    # print('continuing with x y =', x, y)
                    continue
                # print('not continuing with x y =', x, y)
                print_string += paint_print_map[self.map[y, x]]
            print_string += '\n'
        return print_string[:-1]

    def _move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
        extend_idx = -1
        extend_axis = -1
        if self.position[0] < 0:
            extend_idx = 0
            extend_axis = 1
        elif self.position[0] == self.map.shape[1]:
            extend_idx = self.map.shape[1]
            extend_axis = 1
        elif self.position[1] < 0:
            extend_idx = 0
            extend_axis = 0
        elif self.position[1] == self.map.shape[0]:
            extend_idx = self.map.shape[0]
            extend_axis = 0

        if extend_idx >= 0:
            self.map = insert(self.map, extend_idx, -1, extend_axis)
            if extend_idx == 0:
                self.position[0] -= self.direction[0]
                self.position[1] -= self.direction[1]

    def _turn(self, instruction):
        self.direction[0], self.direction[1] = self.direction[1], self.direction[0]
        if instruction:
            self.direction[0] *= -1
        else:
            self.direction[1] *= -1

    def _update(self, instructions):
        # Paint the panel the robot is on
        self.map[int(self.position[1]), int(self.position[0])] = instructions[0]

        # Turn to the left or right
        # Multiplying by 2, then subtracting 1 maps {0, 1} to {-1, 1}
        # -1 means turn left 90 degrees, 1 means turn right 90 degrees
        # self.direction = self.direction.rotate((instructions[1] * 2 - 1) * 90)
        self._turn(instructions[1])

        # Move forward one space
        self._move()

        # Get the color of the space the robot moved to
        return self.map[int(self.position[1]), int(self.position[0])]
