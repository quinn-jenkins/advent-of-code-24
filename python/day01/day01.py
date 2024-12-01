day = "day01"

def extract_two_columns(filename: str):
    with open(filename, 'r') as file:
        column_1 = []
        column_2 = []
        for line in file.readlines():
            line = line.strip()
            a, b = line.split('   ')
            column_1.append(int(a))
            column_2.append(int(b))
    return column_1, column_2

def part_one(filename: str) -> int:
    column_1, column_2 = extract_two_columns(filename)
    column_1.sort()
    column_2.sort()

    total_distance = 0
    for i in range(len(column_1)):
        a = column_1[i]
        b = column_2[i]
        total_distance += abs(a - b)
    return total_distance

def part_two(filename: str) -> int:
    column_1, column_2 = extract_two_columns(filename)

    similarity_score = 0
    similarity_map = dict()
    for num in column_1:
        if num not in similarity_map:
            occurrences = column_2.count(num)
            similarity_map[num] = occurrences
        occurrences = similarity_map[num]
        if occurrences != 0:
            similarity_score += num * occurrences

    return similarity_score


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 11
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 31

    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    