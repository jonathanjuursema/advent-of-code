f = open("input.txt", "r")
raw_grid = f.readlines()


class Grid:
    _grid = []

    def __init__(self, input_data, x_length=None, y_length=None):
        self._grid = []
        if input_data is not None:
            for line in input_data:
                self._grid.append([char for char in line.strip()])
        else:
            self._grid = [['.' for i in range(x_length)] for j in range(y_length)]

    def __eq__(self, other):
        return self._grid == other.get_raw_grid

    @property
    def x_length(self):
        return len(self._grid[0])

    @property
    def y_length(self):
        return len(self._grid)

    def get_cell_value(self, x, y):  # We're using zero-indexing here.
        return self._grid[y][x]

    def set_cell_value(self, x, y, value):
        self._grid[y][x] = value
        pass

    def get_cell_occupied_neighbours(self, x, y):
        occupied = 0
        for dx in [x - 1, x, x + 1]:
            for dy in [y - 1, y, y + 1]:
                if dx == x and dy == y:  # Same cell
                    continue
                elif dx >= self.x_length or dy >= self.y_length or dx < 0 or dy < 0:  # Off grid, zero-index
                    continue
                else:
                    neighbour = self.get_cell_value(x=dx, y=dy)
                    if neighbour == '#':
                        occupied += 1
        return occupied

    @property
    def get_next_iteration(self):
        new_grid = Grid(input_data=None, x_length=self.x_length, y_length=self.y_length)
        for x in range(0, self.x_length):
            for y in range(0, self.y_length):
                cell_value = self.get_cell_value(x, y)
                if cell_value == ".":
                    continue
                n_neighbours = self.get_cell_occupied_neighbours(x, y)
                if cell_value == "L" and n_neighbours == 0:
                    new_grid.set_cell_value(x=x, y=y, value="#")
                elif cell_value == "#" and n_neighbours >= 4:
                    new_grid.set_cell_value(x=x, y=y, value="L")
                else:
                    new_grid.set_cell_value(x=x, y=y, value=cell_value)
        return new_grid

    @property
    def get_raw_grid(self):
        return self._grid.copy()

    @property
    def get_occupied_seats(self):
        return sum([row.count("#") for row in self._grid])

    def print_grid(self):
        print("\n".join(["".join(line) for line in self._grid]) + "\n\n")


grid = Grid(input_data=raw_grid)
while True:
    next_grid = grid.get_next_iteration
    if grid == next_grid:
        break
    grid = next_grid

print("There are {} occupied seats!".format(grid.get_occupied_seats))