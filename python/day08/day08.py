from collections import defaultdict
import itertools

day = "day08"

def is_in_bounds(bounds: tuple, location: tuple) -> bool:
    return location[0] >= 0 and location[1] >= 0 and location[0] <= bounds[0] and location[1] <= bounds[1]

def locate_antennas(lines: list) -> dict:
    antenna_locations = defaultdict(list)
    for row, line in enumerate(lines):
        for col, symbol in enumerate(line):
            if symbol != ".":
                antenna_locations[symbol].append((row, col))
    return antenna_locations

def find_antinodes(antenna_locs: dict, dimensions: tuple) -> list:
    antinodes = set()
    for antenna in antenna_locs.keys():
        antenna_locations = antenna_locs[antenna]
        for pair in list(itertools.combinations(antenna_locations, 2)):
            dx = pair[0][0] - pair[1][0]
            dy = pair[0][1] - pair[1][1]
            potential_antinode_1 = (pair[0][0] + dx, pair[0][1] + dy)
            potential_antinode_2 = (pair[1][0] - dx, pair[1][1] - dy)

            if potential_antinode_1 not in antenna_locations and is_in_bounds(dimensions, potential_antinode_1):
                antinodes.add(potential_antinode_1)
            if potential_antinode_2 not in antenna_locations and is_in_bounds(dimensions, potential_antinode_2):
                antinodes.add(potential_antinode_2)
    return antinodes

def find_antinodes_pt2(antenna_locs: dict, dimensions: tuple) -> list:
    antinodes = set()
    for antenna in antenna_locs.keys():
        antenna_locations = antenna_locs[antenna]
        if len(antenna_locations) >= 2:
            for location in antenna_locations:
                antinodes.add(location)
        for pair in list(itertools.combinations(antenna_locations, 2)):
            dx = pair[0][0] - pair[1][0]
            dy = pair[0][1] - pair[1][1]
            
            potential_antinode = (pair[0][0] + dx, pair[0][1] + dy)
            while is_in_bounds(dimensions, potential_antinode):
                antinodes.add(potential_antinode)
                potential_antinode = (potential_antinode[0] + dx, potential_antinode[1] + dy)
            potential_antinode = (pair[1][0] - dx, pair[1][1] - dy)
            while is_in_bounds(dimensions, potential_antinode):
                antinodes.add(potential_antinode)
                potential_antinode = (potential_antinode[0] - dx, potential_antinode[1] - dy)
    return sorted(antinodes)

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        dimensions = (len(lines)-1, len(lines[0])-1)
        antenna_locations = locate_antennas(lines)
        antinodes = find_antinodes(antenna_locations, dimensions)
        return len(antinodes)

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        dimensions = (len(lines)-1, len(lines[0])-1)
        antenna_locations = locate_antennas(lines)
        antinodes = find_antinodes_pt2(antenna_locations, dimensions)
        return len(antinodes)


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'
    small_ex_file = f'python/{day}/small_example.txt'

    test = part_one(test_file)
    assert test == 14
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 34
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    