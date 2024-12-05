from collections import defaultdict

day = "day05"

def is_update_correct(rules: list, update: list) -> bool:
    for i, page in enumerate(update[:-1]):
        pages_after = update[i+1:]
        for page_after in pages_after:
            if page_after not in rules[page]:
                return False
    return True

def swap_list_elements(update: list, i1, i2):
    update[i2], update[i1] = update[i1], update[i2]
    return update

def fix_wrong_update(rules: list, wrong_update: list) -> list:
    for i, page in enumerate(wrong_update):
        pages_after = wrong_update[i+1:]
        for page_after in pages_after:
            if page_after not in rules[page]:
                return fix_wrong_update(rules, swap_list_elements(wrong_update, i, wrong_update.index(page_after)))
    return wrong_update

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        rules = defaultdict(list)
        comes_before = defaultdict(list)
        updates = []
        reading_rules = True
        for i, line in enumerate(file.readlines()):
            line = line.strip()
            if line == "":
                reading_rules = False
                continue

            if reading_rules:
                first_page, second_page = line.split("|")
                rules[int(first_page)].append(int(second_page))
                comes_before[int(second_page)].append(int(first_page))
            else:
                updates.append([int(x) for x in line.split(",")])

        sum_correct_updates = 0
        for update in updates:
            if is_update_correct(rules, update):
                middle_index = int(len(update) / 2)
                sum_correct_updates += update[middle_index]

        return sum_correct_updates
        
def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        rules = defaultdict(list)
        comes_before = defaultdict(list)
        updates = []
        reading_rules = True
        for i, line in enumerate(file.readlines()):
            line = line.strip()
            if line == "":
                reading_rules = False
                continue

            if reading_rules:
                first_page, second_page = line.split("|")
                rules[int(first_page)].append(int(second_page))
                comes_before[int(second_page)].append(int(first_page))
            else:
                updates.append([int(x) for x in line.split(",")])

        sum_fixed_updates = 0
        for update in updates:
            if not is_update_correct(rules, update):
                fixed_update = fix_wrong_update(rules, update)
                sum_fixed_updates += fixed_update[int(len(fixed_update)/2)]


        return sum_fixed_updates


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 143
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 123
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    