from intcode import IntcodeComputer

if __name__ == '__main__':
    computer = IntcodeComputer()
    computer.load('boost')
    print('KEYCODE:')
    computer.run(1)
    print('COORDINATES:')
    computer.run(2)
