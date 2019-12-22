from painter_bot import PainterBot

if __name__ == '__main__':
    robot = PainterBot()
    print(robot)
    turns = (0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1)
    color = 0
    for x in turns:
        color = (color + 1) % 2
        robot._update((color, x))
        print(robot)
