from collections import defaultdict, deque
from queue import Queue

day = "day10"

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_all_trailheads(grid: list) -> list:
    trailheads = []
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == 0:
                trailheads.append((i, j))
    return trailheads

def find_all_peaks(grid: list) -> list:
    peaks = []
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == 9:
                peaks.append((i, j))
    return peaks

def is_location_in_grid(dimensions: tuple, location: tuple) -> bool:
    return location[0] >= 0 and location[1] >= 0 and location[0] <= dimensions[0] and location[1] <= dimensions[1]

def move_in_direction(current_loc: tuple, direction: tuple) -> tuple:
    return (current_loc[0]+direction[0], current_loc[1]+direction[1])

# since we can only move in directions where the elevation change is exactly 1, 
# we can remove a lot of unnecessary nodes and create a directed graph
def pre_process_grid(grid: list, dimensions: tuple) -> dict:
    graph = defaultdict(list)
    for row, line in enumerate(grid):
        for col, elevation in enumerate(line):
            for direction in directions:
                current_location = (row, col)
                neighbor = move_in_direction(current_location, direction)
                if is_location_in_grid(dimensions, neighbor) and (grid[neighbor[0]][neighbor[1]]) - elevation == 1:
                    graph[(row, col)].append(neighbor)
    return graph

# returns True if it reaches the end, or False if it reaches a point it cannot continue
# goes from the current location and recursively walks the path along each neighbor
def take_next_step(graph: dict, grid: list, current_loc:tuple) -> int:
    current_elevation = grid[current_loc[0]][current_loc[1]]
    if current_elevation == 9:
        return 1
    
    score = 0
    for neighbor in graph[current_loc]:
        score += take_next_step(graph, grid, neighbor)
    return score

# true if there is any path from trailhead to peak
def does_trail_exist(graph: dict, grid: list, trailhead: tuple, peak: tuple) -> bool:
    visited = []
    queue = deque()
    queue.append(trailhead)

    while len(queue) > 0:
        current_loc = queue.popleft()
        visited.append(current_loc)
        current_elevation = grid[current_loc[0]][current_loc[1]]
        if current_loc == peak:
            return True
        neighbors = graph[current_loc]
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
    return False

def calculate_trail_score(graph: dict, grid: list, trailhead: tuple, peaks: list) -> int:
    score = 0
    for peak in peaks:
        if does_trail_exist(graph, grid, trailhead, peak):
            score += 1
    return score

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        grid = []
        for row in file.read().splitlines():
            grid.append([int(col) for col in row])
        trailheads = find_all_trailheads(grid)
        peak_locations = find_all_peaks(grid)
        dimensions = (len(grid)-1, len(grid[0])-1)
        graph = pre_process_grid(grid, dimensions)

        total_score = 0
        for trailhead in trailheads:
            total_score += calculate_trail_score(graph, grid, trailhead, peak_locations)
        return total_score

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        grid = []
        for row in file.read().splitlines():
            grid.append([int(col) for col in row])
        trailheads = find_all_trailheads(grid)
        peak_locations = find_all_peaks(grid)
        dimensions = (len(grid)-1, len(grid[0])-1)
        graph = pre_process_grid(grid, dimensions)

        total_score = 0
        for trailhead in trailheads:
            total_score += take_next_step(graph, grid, trailhead)
        return total_score


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    print(test)
    assert test == 36
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 81
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    