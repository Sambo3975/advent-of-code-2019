from numpy import prod

# opcode 1  2  3  4  5  6  7  8
il = [0, 4, 4, 2, 2, 3, 3, 4, 4]


class IntcodeComputer:
    """Implementation of the incode computer as defined in AoC Day 5"""

    def __init__(self):
        self.ops = [
            None,  # opcode
            self.add,  # 1
            self.mul,  # 2
            self.inp,  # 3
            self.out,  # 4
            self.jit,  # 5
            self.jif,  # 6
            self.lt,  # 7
            self.eq,  # 8
        ]
        self.prog = None  # Program in 'storage'
        self.mem = None  # Program loaded into 'main memory'
        self.ip = 0  # Instruction pointer
        self.jmp = False  # Jump flag; skip the next increment to the instruction pointer if this is set

        # Inputs list. The program will use these as inputs instead of prompting the user, starting at index 0. If
        # another 'inp' operation is run after the end is reached, the user will be prompted
        self.inputs = None
        self.in_ptr = 0  # Pointer to the current position in the input list

        # If true, the program is suspended when an input is needed. To resume operation, call resume(input), with input
        # being the desired input for the suspended instruction
        self.suspend_on_input = False
        self.can_resume = False  # Cannot resume if the program has not started running or has reached the end

    # File parsing and loading #

    def parse(self, string):
        """
        Parse the string into an Intcode memory block. This memory block will not be modified. A fresh copy of it will
        be loaded into self.mem when run() is called
        """
        self.prog = [int(x) for x in string.split(',')]
        self.can_resume = False

    def load(self, name):
        """Load an Intcode file and parse it into the prog block."""
        with open(name + '.int', 'r') as f:
            self.parse(f.read())

    # Execution #

    def _reset(self, inputs):
        self.mem = self.prog.copy()
        self.ip = 0

        if type(inputs) == int:
            self.inputs = [inputs]
        else:
            self.inputs = inputs
        self.in_ptr = 0

        self.can_resume = True

    def _exec(self):
        while True:
            if self.exec_instr():
                return self.mem[0]

    def run(self, inputs=None, suspend_on_input=False):
        """Load the program into 'main memory' and run it"""
        if not self.prog:
            print('No program loaded!')
            return
        self.suspend_on_input = suspend_on_input
        self._reset(inputs)
        return self._exec()

    def resume(self, inputs=None):
        """Run the program from the last place it was suspended"""
        if not self.can_resume:
            print("No program to resume!")
            return

        if type(inputs) == int:
            self.inputs = [inputs]
        else:
            self.inputs = inputs
        self.in_ptr = 0

        return self._exec()

    def exec_instr(self):
        """Run the instruction located at the instruction pointer (ip)"""
        ins = self.mem[self.ip]
        op = ins % 100
        if op == 99:
            self.can_resume = False
            return True  # Signal that the halt instruction was executed
        try:
            ni = il[op]
        except IndexError:
            print('%d: invalid opcode (%d)! Aborting' % (self.ip, op))
            return True
        modes = []  # Read modes: 0 for mem[arg] or 1 for literal arg
        ins //= 10
        for i in range(ni - 1):
            ins //= 10
            modes.append(ins % 10)
        if self.ops[op](modes):
            return True  # Halt due to a suspend
        self.ip += 0 if self.jmp else ni
        self.jmp = False
        return False  # No halt

    # Memory management #

    def read(self, val, mode):
        return val if mode else self.mem[val]

    def get_n_args(self, n, modes):
        return [self.read(self.mem[self.ip + 1 + i], modes[i]) for i in range(n)]

    def write(self, val, loc):
        self.mem[loc] = val

    # Operations #

    def add(self, modes):
        """
        yx01,a,b,c : sum the values at addresses a and b and store the result at address c. x and y control the read
        modes for a and b. If x == 1, the literal value of a is used. same for x and b. This is, in general, how read
        modes work
        """
        args = self.get_n_args(2, modes)
        self.write(sum(args), self.mem[self.ip + 3])

    def mul(self, modes):
        """yx01,a,b,c : store the product of the values at addresses a and b at address c. x,y are mode switches"""
        args = self.get_n_args(2, modes)
        self.write(prod(args), self.mem[self.ip + 3])

    def inp(self, modes):  # Modes are unused, but the signatures of all the operations must be the same
        """3,a : prompt the user for an integer and store it at address a"""
        if self.inputs:
            arg = self.inputs[self.in_ptr]
            self.in_ptr += 1
            if self.in_ptr == len(self.inputs):
                self.inputs = None
        else:
            if self.suspend_on_input:
                return True
            arg = input('> ')

        try:
            self.write(int(arg), self.mem[self.ip + 1])
        except ValueError:
            raise ValueError("Invalid input ('%d')! Aborting..." % arg)

    def out(self, modes):
        """x04,a : print the value at address a using read mode x"""
        print(self.read(self.mem[self.ip + 1], modes[0]))

    def jit(self, modes):
        """yx05,a,b : if the value at address a is nonzero, jump to address b. x,y controls a,b's read mode"""
        args = self.get_n_args(2, modes)
        if args[0]:
            self.ip = args[1]
            self.jmp = True

    def jif(self, modes):
        """yx06,a,b : if the value at address a is zero, jump to address b. x,y controls a,b's read mode"""
        args = self.get_n_args(2, modes)
        if not args[0]:
            self.ip = args[1]
            self.jmp = True

    def lt(self, modes):
        """
        yx07,a,b,c : if the value at address a is less than the value at address b, set the value at c to 1, else set it
        to 0
        """
        args = self.get_n_args(2, modes)
        self.write(1 if args[0] < args[1] else 0, self.mem[self.ip + 3])

    def eq(self, modes):
        """
        yx08,a,b,c : if the value at address a is equal to the value at address b, set the value at c to 1, else set it
        to 0
        """
        args = self.get_n_args(2, modes)
        self.write(1 if args[0] == args[1] else 0, self.mem[self.ip + 3])
