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

def is_guard_in_loop(starting_point: tuple, obstacles: list, dimensions: tuple) -> bool:
    guard_path = [starting_point]
    current_point = starting_point
    current_direction = 0
    while is_in_bounds(dimensions, current_point):
        direction = directions[current_direction]
        next_point = move_in_direction(current_point, direction)
        while (next_point[0], next_point[1]) in obstacles:
            # next_point would hit an obstacle, so instead rotate 90 degrees
            current_direction = (current_direction + 1) % 4
            direction = directions[current_direction]
            next_point = move_in_direction(current_point, direction)
        # should be using a set so we don't have to check this every time, but it doesn't maintain order 
        # so it makes debugging more difficult...
        if next_point not in guard_path:
            if is_in_bounds(dimensions, next_point):
                guard_path.append(next_point)
        else:
            return True
        current_point = next_point
    return False

# def is_guard_in_loop(lines: list) -> bool:
#     obstacles = []
#     starting_point = None
#     for row, line in enumerate(lines):
#         for col, char in enumerate(line):
#             if char == "#":
#                 obstacles.append((row, col))
#             elif char == "^":
#                 starting_point = (row, col, up)

#     guard_path = [starting_point]
#     dimensions = (len(lines)-1, len(lines[0].strip())-1)
#     current_point = starting_point
#     current_direction = 0
#     while is_in_bounds(dimensions, current_point):
#         direction = directions[current_direction]
#         next_point = move_in_direction(current_point, direction)
#         while (next_point[0], next_point[1]) in obstacles:
#             # next_point would hit an obstacle, so instead rotate 90 degrees
#             current_direction = (current_direction + 1) % 4
#             direction = directions[current_direction]
#             next_point = move_in_direction(current_point, direction)
#         # should be using a set so we don't have to check this every time, but it doesn't maintain order 
#         # so it makes debugging more difficult...
#         if next_point not in guard_path:
#             if is_in_bounds(dimensions, next_point):
#                 guard_path.append(next_point)
#         else:
#             return True
#         current_point = next_point
#     return False

def get_obstacles_and_starting_point(lines: list) -> list:
    obstacles = []
    starting_point = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                obstacles.append((row, col))
            elif char == "^":
                starting_point = (row, col, up)
    return obstacles, starting_point

def find_new_obstacle_positions(starting_obstacles: list, guard_path: list, dimensions: tuple) -> int:
    new_obstacle_position = set()
    starting_point = (guard_path[0][0], guard_path[0][1])
    guard_path_length = len(guard_path)
    for i, guard_location in enumerate(guard_path[1:]):
        position = (guard_location[0], guard_location[1])
        if position == starting_point:
            # can't put an obstacle on the guard's starting location
            continue
        print(f"Progress: {i/guard_path_length*100}%")
        if position not in new_obstacle_position and is_guard_in_loop(starting_point, starting_obstacles + [position], dimensions):
            print(f"{position} - {guard_location[2]} created a loop!")
            new_obstacle_position.add(position)
    return len(new_obstacle_position)

def calculate_guard_path(lines: list) -> list:
    obstacles, starting_point = get_obstacles_and_starting_point(lines)
    guard_path = [starting_point]
    dimensions = (len(lines)-1, len(lines[0].strip())-1)
    current_point = starting_point
    current_direction = 0
    while is_in_bounds(dimensions, current_point):
        direction = directions[current_direction]
        next_point = move_in_direction(current_point, direction)
        while (next_point[0], next_point[1]) in obstacles:
            # next_point would hit an obstacle, so instead rotate 90 degrees
            current_direction = (current_direction + 1) % 4
            direction = directions[current_direction]
            next_point = move_in_direction(current_point, direction)
        # should be using a set so we don't have to check this every time, but it doesn't maintain order 
        # so it makes debugging more difficult...
        if next_point not in guard_path:
            if is_in_bounds(dimensions, next_point):
                guard_path.append(next_point)
        current_point = next_point

    return guard_path

def count_unique_guard_positions(guard_path: list) -> int:
    unique_positions = set()
    for position in guard_path:
        unique_positions.add((position[0], position[1]))
    return len(unique_positions)

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        guard_path = calculate_guard_path(lines)
        unique_positions = count_unique_guard_positions(guard_path)
        print(f"Guard travelled to {unique_positions} positions")
        return unique_positions

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        dimensions = (len(lines)-1, len(lines[0].strip())-1)
        obstacles, starting_point = get_obstacles_and_starting_point(lines)
        return find_new_obstacle_positions(obstacles, calculate_guard_path(lines), dimensions)

if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    print(test)
    assert test == 41

    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    print(test)
    assert test == 6
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    