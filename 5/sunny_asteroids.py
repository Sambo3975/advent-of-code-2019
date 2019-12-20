from intcode import IntcodeComputer


if __name__ == '__main__':
    computer = IntcodeComputer()
    computer.load('diag')
    computer.run()
