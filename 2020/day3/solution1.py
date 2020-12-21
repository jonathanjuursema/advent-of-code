f = open("input.txt", "r")
grid = f.readlines()


def get_cell(grid, position):
    width_x = len(grid[0])
    x = position[0] % (width_x - 1)  # grid extends to the right infinitely and zero-index combined with modulo, so -1
    y = position[1]

    print_grid = grid[y][:x] + 'O' + grid[y][x + 1:]
    print(print_grid.rstrip())

    return grid[y][x]


position = [0, 0]
trees = 0

while position[1] < len(grid):  # while still above last row
    cell = get_cell(grid, position)
    if cell == '#':
        trees += 1

    position = [position[0] + 3, position[1] + 1]

print("Encountered {} trees!".format(trees))
