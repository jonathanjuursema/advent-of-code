import copy
import itertools

f = open("input.txt", "r")
input_grid = [[True if coord == "#" else False for coord in list(line.strip())] for line in f.read().splitlines()]


class PocketDimension:

    def __init__(self, dimensions, state={}):
        self._ranges = {}
        self._dimensions = dimensions.copy()
        for d in dimensions:
            self._ranges[d] = (0, 0)
        self._state = state

    def set_starting_grid(self, state):
        for row_index, row in enumerate(state):
            for col_index, field in enumerate(row):
                coord = [col_index, row_index]
                while len(coord) < len(self._dimensions):
                    coord.append(0)
                n_dimensional_coordinate = tuple(coord)
                self.set_coordinate(n_dimensional_coordinate, active=field)

    def _get_coordinate(self, n_dimensional_coordinate):
        try:
            return self._state[",".join([str(i) for i in n_dimensional_coordinate])]
        except:
            return False

    def set_coordinate(self, n_dimensional_coordinate, active):
        self._state[",".join([str(i) for i in n_dimensional_coordinate])] = active
        if active:
            for dim_index, dim_name in enumerate(self._ranges.keys()):
                coord = n_dimensional_coordinate[dim_index]
                if coord < self._ranges[dim_name][0]:
                    self._ranges[dim_name] = (coord, self._ranges[dim_name][1])
                if coord > self._ranges[dim_name][1]:
                    self._ranges[dim_name] = (self._ranges[dim_name][0], coord)

    @property
    def state(self):
        return self._state

    def simulate_cycle(self):
        next_state = PocketDimension(dimensions=self._dimensions.copy(), state=copy.deepcopy(self._state))
        ranges = []
        for dim_name in self._ranges.keys():
            ranges.append([i for i in range(self._ranges[dim_name][0] - 1, self._ranges[dim_name][1] + 2)])
        for n_dimensional_coordinate in itertools.product(*ranges):
            next_state.set_coordinate(n_dimensional_coordinate, self._simulate_cell(n_dimensional_coordinate))
        return next_state

    def _simulate_cell(self, n_dimensional_coordinate):
        active_neighbours = 0
        for delta_coordinates in itertools.product([-1, 0, 1], repeat=len(n_dimensional_coordinate)):
            if set(delta_coordinates) == {0}:
                continue
            if self._get_coordinate(tuple([n_dimensional_coordinate[i] + delta_coordinates[i] for i in
                                           range(0, len(n_dimensional_coordinate))])) is True:
                active_neighbours += 1
        current_state = self._get_coordinate(n_dimensional_coordinate)
        if current_state is True:
            next_state = True if active_neighbours in [2, 3] else False
        elif current_state is False:
            next_state = True if active_neighbours == 3 else False
        return next_state

    def print(self):
        pass
        header = ", ".join(["{}:{}".format(dim_name, self._ranges[dim_name]) for dim_name in self._dimensions])
        print("=== CYCLE | {} ===".format(header))

        non_rendered_range_names = []
        non_rendered_ranges = []
        rendered_ranges = []

        for dim_name in list(self._ranges.keys())[2:]:
            non_rendered_range_names.append(dim_name)
            non_rendered_ranges.append([i for i in range(self._ranges[dim_name][0] - 1, self._ranges[dim_name][1] + 2)])

        for dim_name in list(self._ranges.keys())[:2]:
            rendered_ranges.append([i for i in range(self._ranges[dim_name][0] - 1, self._ranges[dim_name][1] + 2)])

        sub_header = ""
        for non_rendered_coordinates in itertools.product(*non_rendered_ranges):
            sub_header = []
            for i, non_rendered_coordinate in enumerate(non_rendered_coordinates):
                sub_header.append(str("{}={}".format(non_rendered_range_names[i], non_rendered_coordinate)))
            sub_header = ", ".join(sub_header)

            grid = ""
            for y in rendered_ranges[1]:
                row = ""
                for x in rendered_ranges[0]:
                    c = [x, y]
                    c = tuple(c + list(non_rendered_coordinates))
                    row += "#" if self._get_coordinate(c) else "."
                grid += "{}\n".format(row)

            if '#' in grid:
                print(sub_header)
                print(grid)

    @property
    def active_cubes(self):
        active = 0
        ranges = []
        for dim_name in self._ranges.keys():
            ranges.append([i for i in range(self._ranges[dim_name][0] - 1, self._ranges[dim_name][1] + 2)])
        for n_dimensional_coordinate in itertools.product(*ranges):
            if self._get_coordinate(n_dimensional_coordinate) is True:
                active += 1
        return active


dimension = PocketDimension(dimensions=['x', 'y', 'z', 'w'])
dimension.set_starting_grid(state=input_grid)
for i in range(0, 6):
    print("Starting iteration {}...".format(i))
    next_state = dimension.simulate_cycle()
    dimension = next_state

print("There are now {} active cubes.".format(dimension.active_cubes))
