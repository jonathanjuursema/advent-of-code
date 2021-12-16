from math import inf
from queue import PriorityQueue

f = open("input.txt", "r").read()


class Position:
    _x = None
    _y = None
    _risk_level = None
    _neighbours = []

    def __init__(self, x, y, risk_level):
        self._x = x
        self._y = y
        self._risk_level = int(risk_level)
        self._neighbours = []

    def add_neighbour(self, neighbour):
        self._neighbours.append(neighbour)

    @property
    def neighbours(self):
        return self._neighbours

    @property
    def risk_level(self):
        return self._risk_level

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Cave:
    _squares = None
    _distances = None
    _last_cell = None
    _distance_queue = None

    _max_x = None
    _max_y = None

    def __init__(self, puzzle_input):
        puzzle_input = puzzle_input.split("\n")
        # Make a matrix so we can quickly access any cell in the cave.
        self._squares = [[None] * len(puzzle_input[0]) for _ in range(0, len(puzzle_input))]

        self._max_x = len(puzzle_input[0]) - 1
        self._max_y = len(puzzle_input) - 1

        # Make a matrix so we can quickly look-up the shortest distances.
        self._distances = [[None] * len(puzzle_input[0]) for _ in range(0, len(puzzle_input))]
        # In the end we didn't need this property for the puzzle, but it is used to actually trace back the shortest
        # path if we ever want it.
        self._last_cell = [[None] * len(puzzle_input[0]) for _ in range(0, len(puzzle_input))]

        # For part 1, I didn't used a PriorityQueue to keep track of what nodes we still had to visit.
        # Instead, I just kept track of all nodes visited (or kept track of all nodes still to visit), check if
        # they already had a cost associated (so had been "touched") and if so, search for the smallest cost to continue
        # with that node. Of course, this didn't scale at all for part 2. For part 1, this completed in roughly 6s on
        # my hardware.
        # Using a priority queue was not my own idea, but came from looking for ways to make Dijkstra quicker.
        self._distance_queue = PriorityQueue()

        # Initialize all cells with their risk level.
        for y in range(0, self._max_x + 1):
            for x in range(0, self._max_y + 1):
                pos = Position(x=x, y=y, risk_level=puzzle_input[y][x])
                self._squares[y][x] = pos

        # Add neighbours to all cells.
        for y in range(0, self._max_x + 1):
            for x in range(0, self._max_y + 1):
                pos = self._squares[y][x]
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = x + dx
                    ny = y + dy
                    if nx < 0 or nx > self._max_x or ny < 0 or ny > self._max_y:
                        continue
                    neighbour = self._squares[ny][nx]
                    pos.add_neighbour(neighbour)
                # Initialize the smallest distance and previous cell variables.
                self._distances[pos.y][pos.x] = inf
                self._last_cell[pos.y][pos.x] = None

    def explore(self):
        # Dijkstra time! Start at the start position.
        current = self._squares[0][0]
        cost = 0
        self._distances[current.y][current.x] = cost
        self._last_cell[current.y][current.x] = None
        # As long as we haven't reached the end goal...
        while True:
            # From our current node, check in in the neighbours.
            for neighbour in current.neighbours:
                # Calculate the cost to travel to the new cell from the current cell.
                new_cost = cost + neighbour.risk_level
                # If the current route is better, overwrite any previous values for that cell.
                if new_cost < self._distances[neighbour.y][neighbour.x]:
                    self._distances[neighbour.y][neighbour.x] = new_cost
                    self._last_cell[neighbour.y][neighbour.x] = (current.x, current.y)
                    # Put the neighbouring cell on the priority queue to be evaluated in the future.
                    self._distance_queue.put((new_cost, (neighbour.x, neighbour.y)))
            # Get the next node the evaluate, which is the one with the lowest cost.
            next_distance, next_coords = self._distance_queue.get()
            current, cost = self._squares[next_coords[1]][next_coords[0]], next_distance
            # If the "current" cell is the end cell (bottom right), we've found the shortest path!
            if (current.x, current.y) == (self._max_x, self._max_y):
                break
        return cost


cave = Cave(f)
cost = cave.explore()

print('[pt1] Shortest possible distance to the end is: {}'.format(cost))

# Generate the new map. This code is a bit of a mess but I'll try to document it as best I can.
map = f.split("\n")
# dim contains the "size" of the map, to differentiate between example and input.
dim = len(map)

# The "map row" is an intermediate data structure. Due to how the new map is generated, we can generate a longer
# "stretch" based on the initial map, which already gives us the full "width" of the new map. But... if we make it
# longer, we can "shift" the row one block to the left, to get the next 5 "rows" of the map.
# This piece of codes generates the "map row".
new_map_row = []
for line in map:
    # For each line of the initial map...
    new_line = []
    # Convert strings to integers.
    l = [int(c) for c in line]
    # Calculate the next ten "blocks" of the map. For the first "row" we only need 5 blocks, but if we generate this now
    # we can use it later for the "shift" trick.
    for i in range(0, 10):
        # Add the block to the "new blocks".
        new_line.extend([c for c in l])
        # Increase all values with 1.
        l = [c + 1 for c in l]
        # If a value goes over 9, roll back to 1.
        l = [c if c <= 9 else 1 for c in l]
    # Append the line we just generated.
    new_map_row.append(new_line)

# Now that we have our template "map row", we can generate the actual map.
new_map = []
# We need to generate 5 times as many map lines as previously.
for line_no in range(0, dim * 5):
    # The line number that we need to base off from. This rolls over to 0 every "length of the map".
    original_line_no = line_no % dim
    # This is the "shift" trick documented earlier. For each subsequent iteration of the map we want to shift the
    # template to the left one block.
    iteration = line_no // dim
    # This one liner takes a chunk from the template. The chunk starting position is based on the shift trick,
    # and the length is always 5 times the original map size.
    new_map.append(new_map_row[original_line_no][iteration * dim:(iteration * dim) + dim * 5])

# Convert the new map back to a string because that's what the original code used and I'm to lazy to change it now.
map_pt2 = "\n".join("".join(str(c) for c in line) for line in new_map)

# Run part 2.
cave = Cave(map_pt2)
cost = cave.explore()

print('[pt2] Shortest possible distance to the end is: {}'.format(cost))
