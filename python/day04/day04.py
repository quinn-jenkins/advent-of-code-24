import numpy as np

day = "day04"

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

all_directions = [up, down, left, right, tuple(np.add(up,right)), tuple(np.add(up,left)), tuple(np.add(down,right)), tuple(np.add(down,left))]

part_two_directions = [tuple(np.add(up, right)), tuple(np.add(down, right))]
# these are all directions 90 degrees from each other
opposite_directions = {up:right, down:left, 
                      left:down, right:up, 
                      tuple(np.add(up,right)):tuple(np.add(down,right)), tuple(np.add(down,left)):tuple(np.add(up,left)),
                      tuple(np.add(up,left)): tuple(np.add(up,right)), tuple(np.add(down,right)):tuple(np.add(down,left))
                      }
    
def is_location_in_dimension(location:tuple, dimensions:tuple) -> bool:
    return location[0] >= 0 and location[1] >= 0 and location[0] <= dimensions[0] and location[1] <= dimensions[1]

def matches_in_direction(lines: list, dimensions: tuple, x_loc:tuple, direction:tuple):
    for i, next_letter in enumerate("MAS", 1):
        next_letter_loc = (x_loc[0] + i * direction[0], x_loc[1] + i * direction[1])
        if not is_location_in_dimension(next_letter_loc, dimensions):
            return False
        if lines[next_letter_loc[0]][next_letter_loc[1]] != next_letter:
            return False
    return True

# for part one, starting with the location of an 'x', search in all 8 directions and count how many occurrences of "XMAS" there are
def search_around_x(lines: list, dimensions: tuple, x_loc: tuple) -> int:
    xmas_occurrences = 0
    for direction in all_directions:
        if matches_in_direction(lines, dimensions, x_loc, direction):
            xmas_occurrences += 1
    return xmas_occurrences 

def part_two_matches_in_direction(lines: list, dimensions: tuple, a_loc:tuple, direction:tuple):
    first_letter_loc = (a_loc[0] + direction[0], a_loc[1] + direction[1])
    second_letter_loc = (a_loc[0] - direction[0], a_loc[1] - direction[1])
    if not is_location_in_dimension(first_letter_loc, dimensions) or not is_location_in_dimension(second_letter_loc, dimensions):
        return False
    
    first_letter = lines[first_letter_loc[0]][first_letter_loc[1]]
    second_letter = lines[second_letter_loc[0]][second_letter_loc[1]]
    combined = first_letter + "A" + second_letter
    return "MAS" == combined or "MAS" == combined[::-1]

# for part two, starting with the location of an 'a', look in 2 directions (on both sides of the a) for any "MAS". For any that is found, 
# search the opposite direction to see if it is also an "MAS". If so, return True.
def search_around_a(lines: list, dimensions: tuple, a_loc: tuple) -> bool:
    for direction in part_two_directions:
        opposite_direction = opposite_directions[direction]
        if part_two_matches_in_direction(lines, dimensions, a_loc, direction) and part_two_matches_in_direction(lines, dimensions, a_loc, opposite_direction):
            # print(f"Found an X-MAS around {a_loc} (Direction: {direction}, {opposite_direction})")
            return True
    return False

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        xmas_count = 0
        lines = file.readlines()
        dimensions = (len(lines)-1, len(lines[0].strip())-1)
        for row, line in enumerate(lines):
            for col, letter in enumerate(line):
                if letter == 'X':
                    xmas_count += search_around_x(lines, dimensions, (row, col))
        return xmas_count  

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        x_mas_count = 0
        lines = file.readlines()
        dimensions = (len(lines) -1, len(lines[0].strip())-1)
        for row, line in enumerate(lines):
            for col, letter in enumerate(line):
                if letter == 'A':
                    x_mas_count += search_around_a(lines, dimensions, (row, col))
        return x_mas_count  

if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 18
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 9
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    assert p2 < 1909
    