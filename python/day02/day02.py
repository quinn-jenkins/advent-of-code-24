from concurrent.futures import ThreadPoolExecutor

day = "day02"

def read_reports(filename: str) -> list:
    with open(filename, 'r') as file:
        reports = []
        for line in file.readlines():
            numbers = [int(x) for x in line.split()]
            reports.append(numbers)
        return reports
        
def is_report_ascending(report: list) -> bool:
    first = report[0]
    for other in report[1:]:
        if other != first:
            return other > first
    return False

def get_report_without_value(report: list, index: int) -> list:
    if index == 0:
        return report[1:]
    elif index == len(report)-1:
        return report[:-1]
    else:
        return report[:index] + report[index+1:]
    
# tries the list removing 1 element at a time, and if any of those are safe, returns True
def brute_force_ftw(report: list) -> bool:
    for index, _ in enumerate(report):
        if is_report_safe(get_report_without_value(report, index)):
            return True
    return False

def is_report_safe(report: list, allow_one_fail: bool=False) -> bool:
    # print(f"Processing report: {report}")
    ascending = is_report_ascending(report)
    last: int = report[0]
    for num in report[1:]:
        diff = abs(last - num)
        if diff > 3:
            if allow_one_fail:
                return brute_force_ftw(report)
            else:
                # print(f"Report jumps by more than 3 from {last} to {num} -- not safe")
                return False 
        elif diff == 0:
            if allow_one_fail:
                return brute_force_ftw(report)
            else:
                # print(f"Report did not change between {last} and {num} -- not safe")
                return False 
        elif ascending and num < last:
            if allow_one_fail:
                return brute_force_ftw(report)
            else:
                # print(f"Report was ascending, but {last} > {num} -- not safe")
                return False 
        elif (not ascending) and (num > last):
            if allow_one_fail:
                return brute_force_ftw(report)
            else:
                # print(f"Report was descending, but {last} < {num} -- not safe")
                return False 
        
        last = num
    # print("Report is safe")
    return True 

def part_one(filename: str) -> int:
    reports = read_reports(filename)

    with ThreadPoolExecutor(6) as executor:
        futures = [executor.submit(is_report_safe, report) for report in reports]
    return [f.result() for f in futures].count(True)

def part_two(filename: str) -> int:
    reports = read_reports(filename)

    # safe_reports_count = 0
    # for report in reports:
    #     if is_report_safe(report, True):
    #         safe_reports_count += 1
    # return safe_reports_count

    # its actually a bit faster to _not_ thread this solution because the overhead of spinning up the 
    # threads is almost as long as it takes to check them all, but I wanted to try it anyways
    with ThreadPoolExecutor(6) as executor:
        futures = [executor.submit(is_report_safe, report, True) for report in reports]
    return [f.result() for f in futures].count(True)


if __name__ == '__main__':
    test_file = f'python/{day}/test.txt'
    input_file = f'python/{day}/input.txt'
    edge_conditions_file = f'python/{day}/edge_conditions.txt'

    test = part_one(test_file)
    assert test == 2
    p1 = part_one(input_file)
    print(f"Part One: {p1}")

    test = part_two(test_file)
    assert test == 4
    edge_conditions = part_two(edge_conditions_file)
    assert edge_conditions == 10
    p2 = part_two(input_file)
    print(f"Part Two: {p2}")    