from functools import reduce

day = "day15"

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
WALL = "#"
BOX = "O"
BOX_L = "["
BOX_R = "]"
EMPTY = "."
ROBOT = "@"

DIRECTIONS = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1)
}

def create_part_two_warehouse(warehouse: list) -> list:
    for i, row in enumerate(warehouse):
        row = row.replace(WALL, WALL+WALL)
        row = row.replace(BOX, BOX_L+BOX_R)
        row = row.replace(EMPTY, EMPTY+EMPTY)
        row = row.replace(ROBOT, ROBOT+EMPTY)
        warehouse[i] = row
    return warehouse

# look in the direction of movement
# if the next position is empty, move there and return
# if the next position is a wall, don't move, but return
# if the next position is a box, keep looking in that direction until:
#   1) a wall is found, so the moves can't happen, and we return without moving
#   2) a box is found, so we keep looking further in the same direction
#   3) an empty space is found, so we put a box at that empty space, 
#       and replace the first box in the chain with our robot position
def move(warehouse: list, position: tuple, direction: tuple):
    potential_new_robot_pos = move_in_direction(position, direction)
    next_position = potential_new_robot_pos
    obj_at_next_position = warehouse[next_position[0]][next_position[1]]
    # empty space, so just move there and don't rearrange the warehouse
    if obj_at_next_position == EMPTY:
        return next_position, warehouse
    # wall, so we can't move, just return our current position and don't rearrange the warehouse
    elif obj_at_next_position == WALL:
        return position, warehouse
    # its a box, so we need to keep going until we find an empty space or a wall
    else:
        while obj_at_next_position is not EMPTY and obj_at_next_position is not WALL:
            next_position = move_in_direction(next_position, direction)
            obj_at_next_position = warehouse[next_position[0]][next_position[1]]

        # after any boxes that are in front of us is a wall, so we can't move
        if obj_at_next_position == WALL:
            return position, warehouse
        # after any boxes is an empty space, so put a box in the empty space and and empty space 
        # (where the robot is) at the location of the first box
        else:
            update_warehouse(warehouse, next_position, BOX)
            update_warehouse(warehouse, potential_new_robot_pos, EMPTY)
            return potential_new_robot_pos, warehouse
        
def move_pt_2(warehouse: list, position: tuple, direction: tuple):
    potential_new_robot_pos = move_in_direction(position, direction)
    next_position = potential_new_robot_pos
    obj_at_next_position = warehouse[next_position[0]][next_position[1]]
    if obj_at_next_position == EMPTY:
        update_warehouse(warehouse, position, EMPTY)
        update_warehouse(warehouse, next_position, ROBOT)
        return next_position, warehouse
    elif obj_at_next_position == WALL:
        return position, warehouse
    # we hit a box
    else:
        if obj_at_next_position == BOX_L:
            next_pos_l = next_position
            next_pos_r = move_in_direction(next_position, DIRECTIONS[RIGHT])
        else:
            next_pos_l = move_in_direction(next_position, DIRECTIONS[LEFT])
            next_pos_r = next_position
        obj_at_next_l = warehouse[next_pos_l[0]][next_pos_l[1]]
        obj_at_next_r = warehouse[next_pos_r[0]][next_pos_r[1]]
        
        # if we're pushing UP or DOWN, then we have to consider that the boxes are double wide
        # if direction == UP or direction == DOWN:
        potential_box_segments_to_move = []
        if direction == DIRECTIONS[LEFT] or direction == DIRECTIONS[RIGHT]:
            while (obj_at_next_l is not EMPTY and obj_at_next_r is not EMPTY) and (obj_at_next_l is not WALL and obj_at_next_r is not WALL):
                left_segment = (next_pos_l, obj_at_next_l)
                right_segment = (next_pos_r, obj_at_next_r)
                if left_segment not in potential_box_segments_to_move:
                    potential_box_segments_to_move.append(left_segment)
                if right_segment not in potential_box_segments_to_move:
                    potential_box_segments_to_move.append(right_segment)
                # move 2 elements at a time, since we know that if we're up against a box, the other side of the box is the next character, so we can just skip it
                next_pos_l = move_in_direction(next_pos_l, (direction[0], direction[1]))
                next_pos_r = move_in_direction(next_pos_r, (direction[0], direction[1]))
                obj_at_next_l = warehouse[next_pos_l[0]][next_pos_l[1]]
                obj_at_next_r = warehouse[next_pos_r[0]][next_pos_r[1]]

            # none of the boxes we encountered can move, so just return the current state
            if (obj_at_next_l is WALL) or (obj_at_next_r is WALL):
                return position, warehouse
            # we can push all the boxes, so go through each segment and update it
            else:
                for box_segment in potential_box_segments_to_move:
                    box_position = box_segment[0]
                    box_side = box_segment[1]
                    update_warehouse(warehouse, move_in_direction(box_position, direction), box_side)
                update_warehouse(warehouse, position, EMPTY)
                update_warehouse(warehouse, potential_new_robot_pos, ROBOT)
                return potential_new_robot_pos, warehouse
        else:
            # when moving up or down, we need a slightly different behavior as we need to check the 
            # additional width of the boxes we encounter to see if they can move too
            boxes_to_move = []
            adjacent_spaces = [(next_pos_l, obj_at_next_l), (next_pos_r, obj_at_next_r)]
            adjacent_items = [x[1] for x in adjacent_spaces]
            # keep going until we hit a wall or reach a place where every box can move to an empty position
            while WALL not in adjacent_items and (BOX_L in adjacent_items or BOX_R in adjacent_items):
                boxes_to_move.extend(adjacent_spaces)
                adjacent_spaces = get_all_adjacent_items(warehouse, adjacent_spaces, direction)
                adjacent_items = [x[1] for x in adjacent_spaces]

            # we hit a wall, so we can't move
            if WALL in adjacent_items:
                return position, warehouse
            # we found an empty space, so move everything we've seen in the direction
            else:
                for box in boxes_to_move[::-1]:
                    update_warehouse(warehouse, box[0], EMPTY)
                    new_box_pos = move_in_direction(box[0], direction)
                    box_side = box[1]
                    update_warehouse(warehouse, new_box_pos, box_side)
                if warehouse[potential_new_robot_pos[0]][potential_new_robot_pos[1]] == BOX_L:
                    update_warehouse(warehouse, move_in_direction(potential_new_robot_pos, RIGHT), EMPTY)
                elif warehouse[potential_new_robot_pos[0]][potential_new_robot_pos[1]] == BOX_R:
                    update_warehouse(warehouse, move_in_direction(potential_new_robot_pos, LEFT), EMPTY)
                update_warehouse(warehouse, position, EMPTY)
                update_warehouse(warehouse, potential_new_robot_pos, ROBOT)
                return potential_new_robot_pos, warehouse

def get_all_adjacent_items(warehouse: list, boxes: list, direction: tuple) -> list:
    adjacent_items = []
    for box in boxes:
        position = box[0]
        next_position = move_in_direction(position, direction)
        next_item = warehouse[next_position[0]][next_position[1]]
        if (next_position, next_item) not in adjacent_items:
            adjacent_items.append((next_position, next_item))
        if next_item == BOX_L:
            right_position = move_in_direction(next_position, DIRECTIONS[RIGHT])
            right_item = warehouse[right_position[0]][right_position[1]]
            if (right_position, right_item) not in adjacent_items:
                adjacent_items.append((right_position, right_item))
        elif next_item == BOX_R:
            left_position = move_in_direction(next_position, DIRECTIONS[LEFT])
            left_item = warehouse[left_position[0]][left_position[1]]
            if (left_position, left_item) not in adjacent_items:
                adjacent_items.append((left_position, left_item))
    return adjacent_items

def update_warehouse(warehouse: list, position: tuple, item: str) -> list:
    row = warehouse[position[0]]
    warehouse[position[0]] = row[:position[1]] + item + row[position[1]+1:]
    return warehouse

def move_in_direction(position: tuple, direction: tuple) -> tuple:
    return (position[0] + direction[0], position[1] + direction[1])

def find_start(warehouse: list) -> tuple:
    for i, row in enumerate(warehouse):
        for j, col in enumerate(row):
            if warehouse[i][j] == "@":
                return (i, j)

def calculate_gps_sum(warehouse: list) -> int:
    gps_sum = 0
    for i, row in enumerate(warehouse):
        for j, item in enumerate(row):
            if item == BOX:
                gps_sum += 100 * i + j
    return gps_sum

def calculate_gps_sum_pt_2(warehouse: list) -> int:
    gps_sum = 0
    for i, row in enumerate(warehouse):
        for j, item in enumerate(row):
            if item == BOX_L:
                gps_sum += 100 * i + j
    return gps_sum

def part_one(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        divider = lines.index("")
        warehouse = lines[:divider]
        inputs = [x for line in lines[divider+1:] for x in line]
        position = find_start(warehouse)
        # get rid of our robot's symbol
        update_warehouse(warehouse, position, EMPTY)

        for input in inputs:
            position, warehouse = move(warehouse, position, DIRECTIONS[input])
        
        return calculate_gps_sum(warehouse)

def part_two(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.read().splitlines()
        divider = lines.index("")
        warehouse = lines[:divider]
        inputs = [x for line in lines[divider+1:] for x in line]
        warehouse = create_part_two_warehouse(warehouse[:])
        position = find_start(warehouse)
        
        for input in inputs:
            position, warehouse = move_pt_2(warehouse, position, DIRECTIONS[input])

        return calculate_gps_sum_pt_2(warehouse)


if __name__ == '__main__':
    small_test_file = f'python/{day}/test_small.txt'
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    small = part_one(small_test_file)
    assert small == 2028
    test = part_one(test_file)
    assert test == 10092
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    # small_test_file = f'python/{day}/edgecase.txt'
    # small = part_two(small_test_file)
    test = part_two(test_file)
    assert test == 9021
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")
    