filename = 'input.txt'

with open(filename, 'r') as file:
    data = [[l for l in line] for line in file.read().strip().split()]
