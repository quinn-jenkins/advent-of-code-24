day = "day13"

# Use cramer's rule to solve a 2x2 system of equations
def calculate_cost_for_prize(a_x, a_y, b_x, b_y, prize_x, prize_y):
    det = (a_x*b_y - a_y*b_x)
    det_x = (prize_x*b_y - prize_y*b_x)
    det_y = (a_x*prize_y - a_y*prize_x)

    a_presses = det_x / det
    b_presses = det_y / det
    if a_presses.is_integer() and b_presses.is_integer():
        a_presses = int(a_presses)
        b_presses = int(b_presses)
        cost = a_presses * 3 + b_presses
        return cost


def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        total_cost = 0
        for i in range(0, len(lines), 4):
            _, but_a = lines[i].split("Button A: ")
            a_x, a_y = [int(x[2:]) for x in but_a.split(", ")]
            _, but_b = lines[i+1].split("Button B: ")
            b_x, b_y = [int(x[2:]) for x in but_b.split(", ")]
            _, prize = lines[i+2].split("Prize: ")
            prize_x, prize_y = [int(x[2:]) for x in prize.split(", ")]
            cost = calculate_cost_for_prize(a_x, a_y, b_x, b_y, prize_x, prize_y)
            if cost is not None:
                total_cost += cost
            
    return total_cost

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        total_cost = 0
        for i in range(0, len(lines), 4):
            _, but_a = lines[i].split("Button A: ")
            a_x, a_y = [int(x[2:]) for x in but_a.split(", ")]
            _, but_b = lines[i+1].split("Button B: ")
            b_x, b_y = [int(x[2:]) for x in but_b.split(", ")]
            _, prize = lines[i+2].split("Prize: ")
            prize_x, prize_y = [int(x[2:]) for x in prize.split(", ")]
            cost = calculate_cost_for_prize(a_x, a_y, b_x, b_y, prize_x + 10000000000000, prize_y + 10000000000000)
            if cost is not None:
                total_cost += cost
            
    return total_cost


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 480
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    # part 2 doesn't have an expected value today
    # assert test == 123
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    