from intcode import IntcodeComputer
from painter_bot import PainterBot


def test_robot_movement():
    print('ROBOT MOVEMENT:')
    robot = PainterBot()
    print(robot)
    turns = (0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1)
    color = 0
    for x in turns:
        color = (color + 1) % 2
        robot.update((color, x))
        print(robot)


def test_computer():
    print('COMPUTER OUTPUT STORAGE:')
    computer = IntcodeComputer()
    computer.parse('9,11,203,0,22102,2,0,1,204,1,99')
    result = computer.run(12, True, True)
    print(result)  # Should print [24]


def run_tests():
    test_robot_movement()
    test_computer()


if __name__ == '__main__':
    # run_tests()
    painter = PainterBot()
    painter.paint(0)  # Paint the ship starting from a black panel
    print(painter)  # The result is some sort of blob, maybe a map?

    painter = PainterBot()
    painter.paint(1)  # Start from a white panel this time
    print(painter)

    # Count the panels that were painted at least once
    count = 0
    for row in painter.map:
        for val in row:
            count += 1 if val >= 0 else 0

    print(count)
