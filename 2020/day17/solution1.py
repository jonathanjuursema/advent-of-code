import copy

f = open("input.txt", "r")
input_grid = [[True if coord == "#" else False for coord in list(line.strip())] for line in f.read().splitlines()]


# This Pocket Dimension simulator only simulates the z-axis in one way, because the dimension is symmetrical in the
# Z-axis.
# We need to account for that by using abs() (to convert negative z-coordinates to positive ones) in some places, as
# well as using a trick in the counting property.
class PocketDimension:

    def __init__(self, state=[]):
        self._x_range = (0, 0)
        self._y_range = (0, 0)
        self._z_range = (0, 0)
        self._layers = state

    def set_starting_grid(self, state):
        for row_index, row in enumerate(state):
            for col_index, field in enumerate(row):
                self.set_coordinate(x=col_index, y=row_index, z=0, active=field)

    def _get_coordinate(self, x, y, z):
        try:
            return self._layers[abs(z)]["{},{}".format(x, y)]
        except:
            return False

    def set_coordinate(self, x, y, z, active):
        z = abs(z)
        if z >= len(self._layers) or len(self._layers) == 0:
            self._layers.append({})
        self._layers[z]["{},{}".format(x, y)] = active
        if active:
            if z > self._z_range[1]:
                self._z_range = (0, z)
            if x < self._x_range[0]:
                self._x_range = (x, self._x_range[1])
            if x > self._x_range[1]:
                self._x_range = (self._x_range[0], x)
            if y < self._y_range[0]:
                self._y_range = (y, self._y_range[1])
            if y > self._y_range[1]:
                self._y_range = (self._y_range[0], y)

    @property
    def layers(self):
        return self._layers

    def simulate_cycle(self):
        next_state = [copy.deepcopy(layer) for layer in self._layers]
        next_state = PocketDimension(state=next_state)
        for z in range(self._z_range[0], self._z_range[1] + 2):
            for x in range(self._x_range[0] - 1, self._x_range[1] + 2):
                for y in range(self._y_range[0] - 1, self._y_range[1] + 2):
                    next_state.set_coordinate(x, y, z, self._simulate_cell(x, y, z))
        return next_state

    def _simulate_cell(self, x, y, z):
        active_neighbours = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue
                    if self._get_coordinate(x + dx, y + dy, z + dz) is True:
                        active_neighbours += 1
        current_state = self._get_coordinate(x, y, z)
        if current_state is True:
            next_state = True if active_neighbours in [2, 3] else False
        elif current_state is False:
            next_state = True if active_neighbours == 3 else False
        return next_state

    def print(self):
        print("=== x:{}, y:{}, z:{}".format(self._x_range, self._y_range, self._z_range))
        for z in range(self._z_range[0], self._z_range[1] + 2):
            print("z={}".format(z))
            for y in range(self._y_range[0] - 1, self._y_range[1] + 2):
                row = ""
                for x in range(self._x_range[0] - 1, self._x_range[1] + 2):
                    row += "#" if self._get_coordinate(x, y, z) else "."
                print(row)
            print("\n")

    @property
    def active_cubes(self):
        active = 0
        for z in range(self._z_range[0], self._z_range[1] + 2):
            for y in range(self._y_range[0] - 1, self._y_range[1] + 2):
                for x in range(self._x_range[0] - 1, self._x_range[1] + 2):
                    if self._get_coordinate(x, y, z):
                        if z == 0:
                            active += 1
                        else:
                            active += 2
        return active


dimension = PocketDimension()
dimension.set_starting_grid(state=input_grid)
for i in range(0, 6):
    next_state = dimension.simulate_cycle()
    dimension = next_state

print("There are now {} active cubes.".format(dimension.active_cubes))
