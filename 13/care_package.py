from intcode import IntcodeComputer


def test_computer():
    computer = IntcodeComputer()
    computer.parse('109,15,1206,0,14,204,0,22101,-1,0,0,1105,1,2,99,10')
    output = computer.run(store_output=True, suspend_on_output=True)
    print(output)
    while computer.can_resume:
        output = computer.resume()
        print(output)


if __name__ == '__main__':
    test_computer()
