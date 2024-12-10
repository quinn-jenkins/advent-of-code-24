from collections import defaultdict

day = "day09"

EMPTY = "."

def swap_elements(disk_space: list, index_1: int, index_2: int) -> list:
    disk_space[index_1], disk_space[index_2] = disk_space[index_2], disk_space[index_1]
    return disk_space

def reformat_disk(disk_space: list) -> list:
    next_empty_index = disk_space.index(EMPTY)
    for i in reversed(range(len(disk_space))):
        if disk_space[i] != EMPTY:
            next_file_id_index = i
            break
    while next_empty_index < next_file_id_index:
        # swap the file_id into the empty index
        disk_space = swap_elements(disk_space, next_empty_index, next_file_id_index)
        # move from left to right and find the next empty index
        while disk_space[next_empty_index] != EMPTY:
            next_empty_index += 1
        # move from right to left and find the next file ID
        while disk_space[next_file_id_index] == EMPTY:
            next_file_id_index -= 1
        if next_empty_index > next_file_id_index:
            break
    return disk_space

def insert_file(disk_space: list, file: tuple, free_space: tuple) -> list:
    for i in range(free_space[0], free_space[0]+file[1]):
        disk_space[i] = file[2]
    for i in range(file[0], file[0]+file[1]):
        disk_space[i] = EMPTY
    return disk_space

# files_to_move is a list of files to try to move in order as tuple(index, size, file_id)
# free_space_locations is a list of free space blocks in order as tuple(index, size)
def reformat_disk_pt2(disk_space: list, files_to_move: list, free_space_locations: list) -> list:
    while len(files_to_move) > 0:
        file = files_to_move[-1]
        for i, free_space in enumerate(free_space_locations):
            if file[1] <= free_space[1]:
                disk_space = insert_file(disk_space, file, free_space)
                if free_space[1] != file[1]:
                    # there is some leftover free space that should be readded to the list
                    index = free_space[0] + file[1]
                    size = free_space[1] - file[1]
                    free_space_locations.insert(i, (index, size))
                free_space_locations.remove(free_space)
                break
        files_to_move.remove(file)
        
    return disk_space

def expand_disk_format(dense_format: str):
    expanded = []
    reading_file = True
    for index, value in enumerate(dense_format):
        if reading_file:
            file_id = int(index/2)
            for _ in range(int(value)):
                expanded.append(file_id)
        else:
            for _ in range(int(value)):
                expanded.append(EMPTY)
        reading_file = not reading_file
    return expanded

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        disk_map = file.read().strip()
        disk_space = expand_disk_format(disk_map)
        reformatted_disk = reformat_disk(disk_space)
        sum_1 = 0
        for i, ch in enumerate(reformatted_disk):
            if ch is not EMPTY:
                sum_1 += i*ch
        return sum_1
    
def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        disk_map = file.read().strip()
        
        disk_space = []
        # list of free space blocks as tuple(index, size)
        free_space_locations = []
        # list of files as tuple(index, size, file_id)
        files = []
        reading_file = True
        hard_drive_location = 0
        for index, value in enumerate(disk_map):
            size = int(value)
            if reading_file:
                file_id = int(index/2)
                for i in range(size):
                    disk_space.append(file_id)
                files.append((hard_drive_location, size, file_id))
            else:
                for i in range(size):
                    disk_space.append(EMPTY)
                free_space_locations.append((hard_drive_location, size))
            reading_file = not reading_file
            hard_drive_location += size

        reformatted_disk = reformat_disk_pt2(disk_space, files, free_space_locations)
        sum_2 = 0
        for i, ch in enumerate(reformatted_disk):
            if ch is not EMPTY:
                sum_2 += i*ch
        return sum_2

if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file)
    assert test == 1928
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 2858
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
                
    assert p2 == 6423258376982
    