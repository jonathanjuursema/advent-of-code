f = open("input.txt", "r")
tiles_to_flip = f.read().splitlines()


def convert_location_to_coordinate(line):
    x = 0
    y = 0
    i = 0
    while i < len(line):
        if line[i:i + 1] == "e":
            x += 1
            i += 1
        elif line[i:i + 1] == "w":
            x -= 1
            i += 1
        elif line[i:i + 2] == "se":
            x += 0.5
            y += 1
            i += 2
        elif line[i:i + 2] == "sw":
            x -= 0.5
            y += 1
            i += 2
        elif line[i:i + 2] == "ne":
            x += 0.5
            y -= 1
            i += 2
        elif line[i:i + 2] == "nw":
            x -= 0.5
            y -= 1
            i += 2
    return (x, y)


# True = white, False = black
class Floor:

    def __init__(self, initial_instructions):
        self._pattern = {}
        self._day = 0

        for tile in initial_instructions:
            self.flip_tile(x=tile[0], y=tile[1])

    @staticmethod
    def get_coord_string(x, y):
        return "{}_{}".format(float(x), float(y))

    def flip_tile(self, x, y):
        coord_string = Floor.get_coord_string(x=x, y=y)
        current = self.get_tile(x=x, y=y)
        self._pattern[coord_string] = not current

    def get_tile(self, x, y):
        coord_string = Floor.get_coord_string(x=x, y=y)
        if coord_string not in self._pattern.keys():
            return True
        return self._pattern[coord_string]

    @property
    def no_black_tiles(self):
        return sum([1 if tile is False else 0 for tile in self._pattern.values()])


floor = Floor(initial_instructions=[convert_location_to_coordinate(instruction) for instruction in tiles_to_flip])
print("Puzzle answer: {}".format(floor.no_black_tiles))