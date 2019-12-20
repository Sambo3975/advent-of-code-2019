from intcode import IntcodeComputer
import sys
from io import StringIO
from itertools import permutations


def get_best_config():
    old_stdout = sys.stdout  # Store the default standard output

    computer = IntcodeComputer()
    computer.load('amp')

    max_signal = 0
    for p in list(permutations(range(5))):
        output_signal = 0
        for t in range(5):  # for each thruster
            # Output to a new IO buffer so the output of the program can be fed to the next thruster
            result = StringIO()
            sys.stdout = result

            computer.run((p[t], output_signal))
            output_signal = int(result.getvalue())
        max_signal = max(max_signal, output_signal)

    sys.stdout = old_stdout  # Restore stdout to normal operation

    return max_signal


def get_best_config_2():
    old_stdout = sys.stdout
    # initialize a computer for each amplifier
    computers = [IntcodeComputer() for _ in range(5)]
    [c.load('amp') for c in computers]

    max_signal = 0
    for p in list(permutations(range(5, 10))):
        for c, i in zip(computers, range(5)):
            c.run(p[i], True)

        i = 0
        result = None
        while computers[4].can_resume:  # for each feedback loop
            i += 1
            for c in computers:  # for each computer
                inp = 0 if not result else int(result.getvalue())
                result = StringIO()
                sys.stdout = result
                c.resume(inp)
        max_signal = max(int(result.getvalue()), max_signal)

    sys.stdout = old_stdout

    return max_signal


if __name__ == '__main__':
    print(get_best_config())
    print(get_best_config_2())
