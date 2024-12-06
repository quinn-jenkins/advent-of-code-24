import numpy as np

day = "day06"

up = (-1, 0)
down = (1, 0)
right = (0, 1)
left = (0, -1)
directions = [up, right, down, left]

def is_in_bounds(bounds: tuple, location: tuple) -> bool:
    return location[0] >= 0 and location[1] >= 0 and location[0] <= bounds[0] and location[1] <= bounds[1]

def is_potential_obstacle_location(path: list, new_position: tuple) -> bool:
    # if we have been at this location, but facing 90 degrees to the right, 
    # then we can put an obstance in front of us to create a loop
    dir_index = directions.index(new_position[2])
    loop_direction = directions[(dir_index + 1)%4]
    if (new_position[0], new_position[1], loop_direction) in path:
        print(f"Found a potential obstruction at {new_position}")
        return True

def move_in_direction(current_position: tuple, direction: tuple) -> tuple:
    return (current_position[0]+direction[0], current_position[1]+direction[1], direction)

def hits_obstacle(obstacles: list, position: tuple) -> bool:
    return (position[0], position[1]) in obstacles

def find_new_obstacle_positions(lines: list) -> int:
    new_obstacle_count = 0
    obstacles = []
    starting_point = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                obstacles.append((row, col))
            elif char == "^":
                starting_point = (row, col, up)

    guard_path = [starting_point]
    dimensions = (len(lines)-1, len(lines[0].strip())-1)
    current_point = starting_point
    current_direction = 0
    while is_in_bounds(dimensions, current_point):
        direction = directions[current_direction]
        next_point = move_in_direction(current_point, direction)
        # next_point = (tuple(np.add(current_point, direction)), direction)
        while hits_obstacle(obstacles, next_point):
            # next_point would hit an obstacle, so instead rotate 90 degrees
            current_direction = (current_direction + 1) % 4
            direction = directions[current_direction]
            # next_point = (tuple(np.add(current_point, direction)), direction)
            next_point = move_in_direction(current_point, direction)


        if is_in_bounds(dimensions, next_point):
            if is_potential_obstacle_location(guard_path, next_point):
                new_obstacle_count += 1
            guard_path.append(next_point)
            # symbol = "^"
            # if up is direction:
            #     symbol = "^"
            # elif down is direction:
            #     symbol = "v"
            # elif left is direction:
            #     symbol = "<"
            # elif right is direction:
            #     symbol = ">"
        
            # current_line = lines[next_point[0]]
            # updated_line = current_line[:next_point[1]] + symbol + current_line[next_point[1]+1:]
            # lines = lines[:next_point[0]] + [updated_line] + lines[next_point[0]+1:]
        current_point = next_point

    # for line in lines:
    #     print(line)
    return new_obstacle_count

def calculate_guard_path(lines: list) -> list:
    obstacles = []
    starting_point = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                obstacles.append((row, col))
            elif char == "^":
                starting_point = (row, col)

    guard_path = [starting_point]
    dimensions = (len(lines)-1, len(lines[0].strip())-1)
    current_point = starting_point
    current_direction = 0
    while is_in_bounds(dimensions, current_point):
        direction = directions[current_direction]
        next_point = tuple(np.add(current_point, direction))
        while next_point in obstacles:
            # next_point would hit an obstacle, so instead rotate 90 degrees
            current_direction = (current_direction + 1) % 4
            direction = directions[current_direction]
            next_point = tuple(np.add(current_point, direction))
        # should be using a set so we don't have to check this every time, but it doesn't maintain order 
        # so it makes debugging more difficult...
        if next_point not in guard_path:
            if is_in_bounds(dimensions, next_point):
                guard_path.append(next_point)
                symbol = "^"
                if up is direction:
                    symbol = "^"
                elif down is direction:
                    symbol = "v"
                elif left is direction:
                    symbol = "<"
                elif right is direction:
                    symbol = ">"
            
                current_line = lines[next_point[0]]
                updated_line = current_line[:next_point[1]] + symbol + current_line[next_point[1]+1:]
                lines = lines[:next_point[0]] + [updated_line] + lines[next_point[0]+1:]
        current_point = next_point

    for line in lines:
        print(line)
    return guard_path

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        guard_path = calculate_guard_path(lines)
        return len(guard_path)

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        return find_new_obstacle_positions(lines)


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'
    edge_cases_file = f'python/{day}/edge_cases.txt'

    test = part_one(test_file)
    print(test)
    assert test == 41
    # edge_cases = part_one(edge_cases_file)
    # assert edge_cases == 3

    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    print(test)
    assert test == 6
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    