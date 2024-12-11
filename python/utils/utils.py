# Reads a file, returning each line as a string element in a list
def read_file(filename: str) -> list:
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Reads a file assuming each element is an integer separated by the specified 
# delimiter (or a space if none is supplied)    
def read_file_as_ints(filename: str, delimiter=' ') -> list:
    with open(filename, 'r') as file:
        data = []
        for line in file.readlines():
            row = [int(x) for x in line.split(delimiter)]
            data.append(row)
        return data
    
def read_file_as_int_grid(filename: str) -> list:
    with open(filename, 'r') as file:
        data = []
        for row, line in file.read().splitlines():
            data[row] = [int(col) for col in line]
        return data
                

# for a dataset where each row is the same length, returns a tuple of the 
# length and width of the data
def get_dimensions(data: list) -> tuple:
    return (len(data), len(data[0].strip()))

def get_smallest_and_largest_row_lengths(data: list) -> tuple:
    if len(data) == 0:
        return 0
    smallest = largest = len(data[0])
    for row in data[1:]:
        smallest = min(smallest, len(row))
        largest = max(largest, len(row))
    return (smallest, largest)

def is_in_dimension(coord: tuple, dimensions: tuple) -> bool:
    return coord[0] >= 0 and coord[1] >= 0 and coord[0] < dimensions[0] and coord[1] < dimensions[1]    

# if __name__ == '__main__':
#     test_file = f'python/day04/test.txt'

#     dimensions = get_dimensions_equal_length_rows(read_file(test_file))
#     print(dimensions)
#     dimensions = get_smallest_and_largest_row_lengths(read_file(test_file))
#     print(dimensions)