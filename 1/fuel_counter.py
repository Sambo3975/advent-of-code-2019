# Part 1
def get_cargo_fuel():
    with open('input.txt', 'r') as f:
        total_fuel = 0
        for line in f.readlines():
            mass = int(line)
            total_fuel += mass // 3 - 2
        return total_fuel


# Part 2
def get_total_fuel():
    with open('input.txt', 'r') as f:
        total_fuel = 0
        for line in f.readlines():
            fuel_mass = int(line) // 3 - 2
            while fuel_mass > 0:
                total_fuel += fuel_mass
                fuel_mass = fuel_mass // 3 - 2
        return total_fuel


def main():
    print(get_total_fuel())


if __name__ == '__main__':
    main()
