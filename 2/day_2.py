from colorama import Fore, Style


# Part 1
def load_program(filename):
    with open(filename, 'r') as f:
        return [int(x) for x in f.read().split(',')]


def print_diagnostic(program, pos):
    if pos+3 < len(program):
        print('[', end='')
        argpos1 = program[pos+1]
        argpos2 = program[pos+2]
        respos = program[pos+3]
        for i in range(len(program)):
            if i == pos:
                print(Fore.BLUE + str(program[i]), end=', ')
            elif i == respos:
                print(Fore.YELLOW + str(program[i]), end=', ')
            elif i == argpos1:
                print(Fore.CYAN + str(program[i]), end=', ')
            elif i == argpos2:
                print(Fore.CYAN + str(program[i]), end=', ')
            else:
                print(Style.RESET_ALL + str(program[i]), end=', ')
        print(Style.RESET_ALL + ']')
    else:
        print(program)


def run_intcode(program):
    pos = 0
    while True:
        op = program[pos]
        if op == 99:
            break
        elif op == 1 or op == 2:
            # print_diagnostic(program, pos)
            arg1 = program[program[pos+1]]
            arg2 = program[program[pos+2]]
            program[program[pos+3]] = arg1 + arg2 if op == 1 else arg1 * arg2
            pos += 4
        else:
            raise ValueError("pos %d: Invalid opcode: %d" % (pos, op))
    # print_diagnostic(program, pos)
    return program[0]


def run_program(program, in1, in2):
    resident_program = program.copy()
    if in1:
        resident_program[1] = in1
    if in2:
        resident_program[2] = in2
    return run_intcode(resident_program)


# Part 2
def find_values():
    program = load_program('input.txt')
    for i in range(99):
        for j in range(99):
            if run_program(program, i, j) == 19690720:
                return 100 * i + j


def main():
    print(find_values())


if __name__ == '__main__':
    main()
