import re

day = "day03"

regex_pt1 = r'mul\(\d+,\d+\)'
regex_pt2 = r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)'

def get_uncorrupted_instructions(filename: str, regex) -> list:
    with open(filename, 'r') as file:
        return re.findall(regex, file.read())  

def part_one(filename: str) -> int:
    instructions = get_uncorrupted_instructions(filename, regex_pt1)
    sum = 0
    for instruction in instructions:
        inside_parens = instruction[4:-1]
        x, y = [int(split) for split in inside_parens.split(",")]
        sum += x * y
    return sum

def part_two(filename: str) -> int:
    instructions = get_uncorrupted_instructions(filename, regex_pt2)
    sum = 0
    enabled = True
    for instruction in instructions:
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        else:
            if enabled:
                inside_parens = instruction[4:-1]
                x, y = [int(split) for split in inside_parens.split(",")]
                sum += x * y
    return sum


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 161
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 48
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    