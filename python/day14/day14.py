from collections import defaultdict

day = "day14"

def move(pos: tuple, vel: tuple, dimensions: tuple, num_moves: int) -> tuple:
    current_pos = pos
    for _ in range(num_moves):
        new_row = (current_pos[0] + vel[0]) % dimensions[0]
        new_col = (current_pos[1] + vel[1]) % dimensions[1]
        current_pos = (new_row, new_col)
    return current_pos

def get_safety_factor(robot_positions: list, dimensions: tuple) -> int:
    q1, q2, q3, q4 = [], [], [], []
    middle_row = int(dimensions[0] / 2)
    middle_col = int(dimensions[1] / 2)
    for robot_pos in robot_positions:
        if robot_pos[0] < middle_row and robot_pos[1] < middle_col:
            q1.append(robot_pos)
        elif robot_pos[0] < middle_row and robot_pos[1] > middle_col:
            q2.append(robot_pos)
        elif robot_pos[0] > middle_row and robot_pos[1] > middle_col:
            q3.append(robot_pos)
        elif robot_pos[0] > middle_row and robot_pos[1] < middle_col:
            q4.append(robot_pos)
        # robot is ignored if it falls exactly on a quadrant line in either direction

    return len(q1) * len(q2) * len(q3) * len(q4)

def print_robots(dimensions: tuple, robots: dict):
    for row in range(dimensions[0]):
        for col in range(dimensions[1]):
            if (row, col) in robots.keys():
                print("X", end="")
            else:
                print(".", end="")
        print("")

def part_one(filename: str, dimensions: tuple) -> int:
    end_positions = []
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        for line in lines:
            pos_text, vel_text = line.split(" ")
            pos_y, pos_x = [int(x) for x in pos_text[2:].split(",")]
            vel_y, vel_x = [int(x) for x in vel_text[2:].split(",")]
            end_positions.append(move((pos_x, pos_y), (vel_x, vel_y), dimensions, 100))
        return get_safety_factor(end_positions, dimensions) 

def part_two(filename: str, dimensions: tuple) -> int:
    end_positions = []
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        for line in lines:
            pos_text, vel_text = line.split(" ")
            pos_y, pos_x = [int(x) for x in pos_text[2:].split(",")]
            vel_y, vel_x = [int(x) for x in vel_text[2:].split(",")]
            end_positions.append(move((pos_x, pos_y), (vel_x, vel_y), dimensions, 100))

        robots = defaultdict(list)
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            for line in lines:
                pos_text, vel_text = line.split(" ")
                pos_y, pos_x = [int(x) for x in pos_text[2:].split(",")]
                vel_y, vel_x = [int(x) for x in vel_text[2:].split(",")]
                robots[(pos_x, pos_y)].append((vel_x, vel_y))
            
            for sec in range(1000):
                # Not sure if it is unique to each user's input, but for mine at 11 seconds 
                # there was a weird looking frame that stood out because there was a cluster
                # of robots forming in some of the columns, and not much in the rest of the grid
                # I then noticed that every 101 seconds after that (so 112, 213, ...) a similar pattern appeared,
                # so here I'm just printing every 101st frame starting with the 11th and manually scanning through the 
                # results to see the tree
                if (sec-11) % 101 == 0:
                    print(f"After {sec} seconds:")
                    print_robots(dimensions, robots)
                updated_robots = defaultdict(list)
                for robot_pos in robots:
                    for robot_vel in robots[robot_pos]:
                        updated_pos = move(robot_pos, robot_vel, dimensions, 1)
                        updated_robots[updated_pos].append(robot_vel)
                robots = updated_robots



if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'

    test = part_one(test_file, (7, 11))
    assert test == 12
    p1 = part_one(input_file, (103, 101))
    print(f"Part One: {p1}")

    # test = part_two(test_file)
    # no example value provided today
    # assert test == 123
    p2 = part_two(input_file, (103, 101))
    print(f"Part Two: {p2}")
    