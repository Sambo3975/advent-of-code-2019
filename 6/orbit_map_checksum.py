def count_orbits(data):
    total = 0
    for k in data.keys():
        if k != 'COM':
            subtotal = 1
            nxt = data[k]
            while nxt != 'COM':
                subtotal += 1
                nxt = data[nxt]
            total += subtotal
    return total


def load_orbits(filename):
    orbit_dict = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            pair = line.split(')')
            orbit_dict[pair[1].replace('\n', '')] = pair[0]
    return orbit_dict


def pos_in_transfers(pos, transfers):
    for i in range(len(transfers)):
        if transfers[i][0] == pos:
            return i
    return -1


def count_transfers(data, p1, p2):
    transfers = []
    count = 0
    pos = data[p1]
    while pos != 'COM':
        count += 1
        pos = data[pos]
        transfers.append((pos, count))

    count = 0
    pos = data[p2]
    index = pos_in_transfers(pos, transfers)
    while index < 0:
        pos = data[pos]
        index = pos_in_transfers(pos, transfers)
        count += 1

    return count + transfers[index][1]


if __name__ == '__main__':
    # Part 1
    print(count_orbits(load_orbits('orbits.txt')))
    # Part 2
    print(count_transfers(load_orbits('orbits.txt'), 'YOU', 'SAN'))

