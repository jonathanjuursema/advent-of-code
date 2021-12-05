import numpy as np

f = open("input.txt", "r")
lines = [line.strip("\n") for line in f.readlines()]


class Map:
    _map = None

    # Initialize the ocean floor map.
    def __init__(self, x_len, y_len):
        pass
        self._map = np.zeros((x_len, y_len)).astype(int)

    def add(self, start, end):
        x_direction = +1 if start[0] < end[0] else -1
        y_direction = +1 if start[1] < end[1] else -1

        # Determine the x-coordinates for this line.
        if start[0] == end[0]:
            # The x-coordinate stays the same, make a list of the same length as the line with that x-coordinate.
            x_coordinates = [start[0]] * (abs(start[1] - end[1]) + 1)
        else:
            # The x-coordinate changes. Make a list with all desired x-coordinates.
            x_coordinates = [c for c in range(start[0], end[0] + x_direction, x_direction)]

        # Do the same for the y-coordinates.
        if start[1] == end[1]:
            # The x-coordinate stays the same, make a list of the same length as the line with that x-coordinate.
            y_coordinates = [start[1]] * (abs(start[0] - end[0]) + 1)
        else:
            # The x-coordinate changes. Make a list with all desired x-coordinates.
            y_coordinates = [c for c in range(start[1], end[1] + y_direction, y_direction)]

        a = 0

        for i in range(len(x_coordinates)):
            self._map[(y_coordinates[i], x_coordinates[i])] = self._map[(y_coordinates[i], x_coordinates[i])] + 1

    def count_dangerous_areas(self):
        return np.count_nonzero(self._map >= 2)

    def print(self):
        for row in self._map:
            print("".join(["  ." if cell == 0 else "{:3}".format(cell) for cell in row]))


def parse_line(line):
    positions = line.split(" -> ")
    start = [int(pos) for pos in positions[0].split(",")]
    end = [int(pos) for pos in positions[1].split(",")]
    return start, end


# First, determine the bounds of the map.
max_x = 0
max_y = 0
for line in lines:
    parsed_line = parse_line(line)

    max_x = max(parsed_line[0][0], parsed_line[1][0], max_x)
    max_y = max(parsed_line[0][1], parsed_line[1][1], max_y)

map_part_1 = Map(x_len=max_x + 1, y_len=max_y + 1)
map_part_2 = Map(x_len=max_x + 1, y_len=max_y + 1)

# Then, draw the lines.
for line in lines:
    parsed_line = parse_line(line)

    # For part 1 we only work with horizontal lines.
    if parsed_line[0][0] == parsed_line[1][0] or parsed_line[0][1] == parsed_line[1][1]:
        map_part_1.add(start=parsed_line[0], end=parsed_line[1])

    # For part 2 we work with all lines.
    map_part_2.add(start=parsed_line[0], end=parsed_line[1])

# Print the maps. Commented out for full input.
# print("Part 1 ---\n")
# map_part_1.print()
# print("\nPart 2 ---\n")
# map_part_2.print()
# print("\n----------\n")

# Now, count the number of cells in the map that have a value larger than 2.
print("There are {} dangerous areas, where at least 2 lines of vents overlap, in part 1".format(
    map_part_1.count_dangerous_areas()))
print("There are {} dangerous areas, where at least 2 lines of vents overlap, in part 2".format(
    map_part_2.count_dangerous_areas()))
