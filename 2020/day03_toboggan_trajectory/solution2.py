from numpy import prod

f = open("input.txt", "r")
grid = f.readlines()


def get_cell(grid, position):
    width_x = len(grid[0])
    x = position[0] % (width_x - 1)  # grid extends to the right infinitely and zero-index combined with modulo, so -1
    y = position[1]

    return grid[y][x]


def simulate_route(grid, slope):
    position = [0, 0]
    trees = 0

    while position[1] < len(grid):  # while still above last row
        cell = get_cell(grid, position)
        if cell == '#':
            trees += 1

        position = [position[0] + slope[0], position[1] + slope[1]]

    return trees


slopes = [
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [1, 2]
]

trees = []
for slope in slopes:
    t = simulate_route(grid, slope)
    print("Encountered {} trees on slope {}.".format(t, slope))
    trees.append(t)

print("Product is {}!".format(prod(trees)))
