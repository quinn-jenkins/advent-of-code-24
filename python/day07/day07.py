day = "day07"

def calculate(numbers: list):
    if len(numbers) == 1:
        return numbers

    # add and multiply the first 2 elements in the list, 
    # and then replace those 2 elements with the sum/product until we're out of numbers
    sum_first_elements = numbers[0] + numbers[1]
    product_first_elements = numbers[0] * numbers[1]

    return (calculate([sum_first_elements] + numbers[2:]) +
            calculate([product_first_elements] + numbers[2:]))

def calculate_part_2(numbers: list):
    if len(numbers) == 1:
        return numbers

    # add, multiply, and concatenate the first 2 elements in the list, 
    # and then replace those 2 elements with the sum/product/concat until we're out of numbers
    sum_first_elements = numbers[0] + numbers[1]
    product_first_elements = numbers[0] * numbers[1]
    concat_first_elements = int(str(numbers[0]) + str(numbers[1]))

    return (calculate_part_2([sum_first_elements] + numbers[2:]) +
            calculate_part_2([product_first_elements] + numbers[2:]) +
            calculate_part_2([concat_first_elements] + numbers[2:]))

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        sum_1 = 0
        for line in file.readlines():
            total_text, numbers_text = line.split(": ")
            cal_total = int(total_text)
            numbers = [int(x) for x in numbers_text.split()]
            results = calculate(numbers)
            if cal_total in results:
                sum_1 += cal_total
        return sum_1

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        sum_1 = 0
        for line in file.readlines():
            total_text, numbers_text = line.split(": ")
            cal_total = int(total_text)
            numbers = [int(x) for x in numbers_text.split()]
            results = calculate_part_2(numbers)
            if cal_total in results:
                sum_1 += cal_total
        return sum_1


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 3749
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 11387
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    