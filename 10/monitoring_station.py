from math import sqrt, pi
from numpy import array, copy, full, arctan2
from termcolor import colored


class Target:
    def __init__(self, x, y):
        self.rho, self.phi = cart2pol(x, y)  # Convert to polar
        self.phi += pi / 2  # Convert from standard position to (up = 0, clockwise is positive)
        self.x, self.y = x, y

    def __lt__(self, other):
        if self.phi == other.phi:
            return self.rho < other.rho
        return self.phi < other.phi

    def __repr__(self):
        return 'polar=(%f, %f), cartesian=(%d, %d)' % (self.rho, self.phi, self.x, self.y)


def read_asteroid_data(filename):
    with open(filename, 'r') as f:
        data = []
        for line in f.readlines():
            line_data = []
            for c in line:
                if c != '\n':
                    line_data.append(c == '#')
            data.append(line_data)
    return array(data, dtype=bool)


def gcd(x, y):
    """Compute the GCD of x and y using the Euclidean Algorithm"""
    while y:
        x, y = y, x % y
    return x


def print_data(data):
    for r in range(data.shape[0]):
        print('[', end='')
        for c in range(data.shape[1]):
            print('#' if data[r, c] else '.', end='')
        print(']')
    print()


def count_detectable_asteroids(data, station_r, station_c):
    data = copy(data)
    count = 0
    for r in range(data.shape[0]):
        for c in range(data.shape[1]):
            if data[r, c] and (station_r != r or c != station_c):
                data[r, c] = False
                count += 1
                # get the vertical and horizontal differences between the asteroid's position and the station's position
                step_r = r - station_r
                step_c = c - station_c
                # Treat it as a ratio and reduce to simplest terms
                gcd_rc = abs(gcd(step_r, step_c))
                step_r //= gcd_rc
                step_c //= gcd_rc

                scan_r = station_r + step_r
                scan_c = station_c + step_c
                while 0 <= scan_r < data.shape[0] and 0 <= scan_c < data.shape[1]:
                    if data[scan_r, scan_c]:
                        data[scan_r, scan_c] = False
                    scan_r += step_r
                    scan_c += step_c

    return count


def find_best_station(data):
    max_r = -1
    max_c = -1
    max_count = 0
    for r in range(data.shape[0]):
        for c in range(data.shape[1]):
            if data[r, c]:
                count = count_detectable_asteroids(data, r, c)
                if count > max_count:
                    max_count = count
                    max_r = r
                    max_c = c
    return max_c, max_r, max_count


def collect_targets(data, station_x, station_y):
    """Collect the targets from the given data and the station position"""
    targets = []
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y, x] and (x != station_x or y != station_y):
                targets.append(Target(x - station_x, y - station_y))
    return sorted(targets)


def destroy_targets(targets, data, station_x, station_y):
    destroy_order = full(data.shape, -1, dtype=int)
    destroy_order[station_y, station_x] = -2
    angle = -0.00001
    idx = 0
    remaining = min(len(targets), 200)
    while True:
        t = targets[idx]
        if t and t.phi > angle:
            destroy_order[t.y + station_y, t.x + station_x] = len(targets) - remaining
            targets[idx] = None
            remaining -= 1
            if not remaining:
                return t.x + station_x, t.y + station_y, destroy_order
            angle = t.phi
        idx = (idx + 1) % len(targets)
        if idx == 0:
            angle = -2 * pi


def cart2pol(x, y):
    """Convert Cartesian coordinates to polar"""
    rho = sqrt(x**2 + y**2)
    phi = arctan2(y, x)
    return rho, phi


def print_blowup_data(data):
    print('Blow-up data (+0 ' + colored('+10 ', 'red') + colored('+20 ', 'yellow') + colored('+30', 'blue') + '):')
    for y in range(data.shape[0]):
        print('[', end='')
        for x in range(data.shape[1]):
            d = data[y, x]
            if d == -2:
                print('X', end='')
            elif d >= 30:
                print(colored(d % 10, 'blue'), end='')
            elif d >= 20:
                print(colored(d % 10, 'yellow'), end='')
            elif d >= 10:
                print(colored(d % 10, 'red'), end='')
            elif d >= 0:
                print(d, end='')
            else:
                print('.', end='')
        print(']')


if __name__ == '__main__':
    # Part 1
    asteroid_data = read_asteroid_data('asteroids.txt')
    best_x, best_y, best_count = find_best_station(asteroid_data)
    print('Best is %d,%d with %d other asteroids detected' % (best_x, best_y, best_count))

    # Part 2
    targets = collect_targets(asteroid_data, best_x, best_y)
    tx, ty, destroy_data = destroy_targets(targets, asteroid_data, best_x, best_y)
    print('Last asteroid destroyed was at (%d, %d)' % (tx, ty))
    # print_blowup_data(destroy_data)  # only works on smaller examples
