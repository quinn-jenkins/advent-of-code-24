day = "day12"

# right, down, left, up -- order is important for part 2 when walking the perimeter
directions = [(0, 1), (-1, 0), (0, -1), (1,0)]
diagonals = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

def is_in_garden(garden: list, location: tuple) -> bool:
    return location[0] >= 0 and location[1] >= 0 and location[0] < len(garden) and location[1] < len(garden[0])

def get_neighbor_plants(garden: list, plant: str, location: tuple) -> list:
    neighbors = []
    for direction in directions:
        neighbor_location = get_location_in_direction(location, direction)
        if is_in_garden(garden, neighbor_location) and garden[neighbor_location[0]][neighbor_location[1]] == plant:
            neighbors.append(neighbor_location)
    return neighbors

def get_connected_plants(garden: list, plant: str, location: tuple) -> list:
    plot = [location]
    # these are plants that we've added to the plot already, but we haven't checked if their neighbors are also part of the plot
    check_neighbors = [location]

    while len(check_neighbors) > 0:
        current_plant_loc = check_neighbors.pop()
        neighbors = get_neighbor_plants(garden, plant, current_plant_loc)
        for neighbor in neighbors:
            if neighbor not in plot:
                plot.append(neighbor)
                check_neighbors.append(neighbor)
    return sorted(plot)

def get_location_in_direction(location: tuple, direction: tuple) -> tuple:
    return (location[0] + direction[0], location[1] + direction[1])

def get_adjacent_locations(location: tuple) -> list:
    adjacent_locs = []
    for direction in directions:
        adjacent_locs.append(get_location_in_direction(location, direction))
    return adjacent_locs

def get_perimeter(plot: list) -> int:
    perimeter = 0
    for plant in plot:
        adjacent_locations = get_adjacent_locations(plant)
        for loc in adjacent_locations:
            if loc not in plot:
                perimeter += 1
    return perimeter

def get_num_sides(garden: list, plot: list) -> int:
    # the number of sides is equal to the number of corners
    num_turns = 0
    for plant in plot:
        for diagonal_direction in diagonals:
            diagonal_pos = get_location_in_direction(plant, diagonal_direction)
            adjacent_1 = get_location_in_direction(plant, (diagonal_direction[0], 0))
            adjacent_2 = get_location_in_direction(plant, (0, diagonal_direction[1]))
            diag_in_plot = diagonal_pos in plot and is_in_garden(garden, diagonal_pos)
            adj_1_in_plot = adjacent_1 in plot and is_in_garden(garden, adjacent_1)
            adj_2_in_plot = adjacent_2 in plot and is_in_garden(garden, adjacent_2)
            # is a corner if none of the 3 points is in the plot (outer)
            if not diag_in_plot and not adj_1_in_plot and not adj_2_in_plot:
                num_turns += 1
            # is a corner the diagonal is out, but the 2 adjacent are in (inner)
            if not diag_in_plot and adj_1_in_plot and adj_2_in_plot:
                num_turns += 1
            # edge case: diagonal is in, but both adjacent are out
            if diag_in_plot and not adj_1_in_plot and not adj_2_in_plot:
                num_turns += 1

    return num_turns

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        garden = [line.strip() for line in file.readlines()]
        already_counted = []
        total_price = 0
        for row, line in enumerate(garden):
            for col, plant in enumerate(line):
                position = (row, col)
                if position not in already_counted:
                    plot = get_connected_plants(garden, plant, position)
                    # print(f"Plant {plant} at {position} produces plot {plot}")
                    perimeter = get_perimeter(plot)
                    area = len(plot)
                    # print(f"Perimeter: {perimeter} * Area: {area} = {area * perimeter}")
                    total_price += perimeter * area # price = perimeter * area
                    already_counted.extend(plot)
        print(f"Total price in file: {filename} is: {total_price}")
        return total_price

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        garden = [line.strip() for line in file.readlines()]
        already_counted = []
        total_price = 0
        for row, line in enumerate(garden):
            for col, plant in enumerate(line):
                position = (row, col)
                if position not in already_counted:
                    plot = get_connected_plants(garden, plant, position)
                    # print(f"Plant {plant} at {position} produces plot {plot}")
                    num_sides = get_num_sides(garden, plot)
                    area = len(plot)
                    # print(f"Num Sides: {num_sides} * Area: {area} = {area * num_sides}")
                    total_price += num_sides * area # price = num_sides * area
                    already_counted.extend(plot)
        # print(f"Total price in file: {filename} is: {total_price}")
        return total_price


if __name__ == '__main__':
    small_test_file = f'python/{day}/test_small.txt'
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    small = part_one(small_test_file)
    assert small == 140
    test = part_one(test_file)
    assert test == 1930
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    small = part_two(small_test_file)
    assert small == 80
    test = part_two(test_file)
    assert test == 1206
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    