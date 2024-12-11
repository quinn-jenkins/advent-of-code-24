day = "day11"

def split_stone(stone: int) -> list:
    as_string = str(stone)
    split_index = int(len(as_string) / 2)
    first_half = int(as_string[:split_index])
    second_half = int(as_string[split_index:])
    return [first_half, second_half]

def transform_stone(stone: int) -> list:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        return split_stone(stone)
    else:
        return [2024 * stone]

def blink(stones: list) -> list:
    updated_stones = []
    for stone in stones:
        updated_stones.extend(transform_stone(stone))
    return updated_stones

def blink_x_times(stones: list, blinks: int) -> list:
    for _ in range(blinks):
        stones = blink(stones)
    return stones

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        stones = [int(x) for x in file.read().strip().split(" ")]
        return len(blink_x_times(stones, 25))

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        stones = [int(x) for x in file.read().strip().split(" ")]
        
        stone_count = {}
        for stone in stones:
            stone_count[stone] = stone_count.get(stone, 0) + 1

        for _ in range(75):
            updated_stones = {}

            for key, value in stone_count.items():
                transformed = transform_stone(key)
                for stone in transformed:
                    updated_stones[stone] = updated_stones.get(stone, 0) + value
            stone_count = updated_stones
        return sum(stone_count.values())

if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 55312
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    # not actually provided today...
    assert test == 65601038650482
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    