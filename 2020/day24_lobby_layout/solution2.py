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
            self.flip_tile(coordinate=tile)

    def iterate(self):
        new_pattern = {}
        # Check all "known" tiles.
        for tile in [Floor.parse_coord_string(tile_string) for tile_string in self._pattern.keys()]:
            coord_string = Floor.get_coord_string(coordinate=tile)
            if coord_string not in new_pattern.keys():
                new_pattern[coord_string] = self.determine_new_tile_color(coordinate=tile)

            # However, there are also white tiles that we haven't "visited" yet, that might eligble to flip.
            # Let's make sure we have checked all neighbours for this tile as well to catch the edge cases.
            for neighbour in Floor.get_neigbour_coordinates(coordinate=tile):
                neighbour_coord_string = Floor.get_coord_string(coordinate=neighbour)
                if neighbour_coord_string not in new_pattern.keys():
                    new_pattern[neighbour_coord_string] = self.determine_new_tile_color(coordinate=neighbour)

        self._pattern = new_pattern

    def determine_new_tile_color(self, coordinate):
        n_black_neighours = self.no_black_neighours(coordinate=coordinate)
        current_tile_color = self.get_tile(coordinate=coordinate)
        if current_tile_color is False and (n_black_neighours == 0 or n_black_neighours > 2):
            new_tile_color = True
        elif current_tile_color is True and n_black_neighours == 2:
            new_tile_color = False
        else:
            new_tile_color = current_tile_color
        return new_tile_color

    @staticmethod
    def get_neigbour_coordinates(coordinate):
        x = coordinate[0]
        y = coordinate[1]
        return [
            (x + 1, y),
            (x - 1, y),
            (x + 0.5, y + 1),
            (x - 0.5, y + 1),
            (x + 0.5, y - 1),
            (x - 0.5, y - 1)
        ]

    def no_black_neighours(self, coordinate):
        black_neighbours = 0
        for neighbour in Floor.get_neigbour_coordinates(coordinate):
            if self.get_tile(coordinate=neighbour) is False:
                black_neighbours += 1
        return black_neighbours

    @staticmethod
    def get_coord_string(coordinate):
        return "{}_{}".format(float(coordinate[0]), float(coordinate[1]))

    @staticmethod
    def parse_coord_string(s):
        l = s.split("_")
        return (float(l[0]), float(l[1]))

    def flip_tile(self, coordinate):
        coord_string = Floor.get_coord_string(coordinate=coordinate)
        current = self.get_tile(coordinate=coordinate)
        self._pattern[coord_string] = not current

    def get_tile(self, coordinate):
        coord_string = Floor.get_coord_string(coordinate)
        if coord_string not in self._pattern.keys():
            return True
        return self._pattern[coord_string]

    @property
    def no_black_tiles(self):
        return sum([1 if tile is False else 0 for tile in self._pattern.values()])


floor = Floor(initial_instructions=[convert_location_to_coordinate(instruction) for instruction in tiles_to_flip])
print("Day 0: {}".format(floor.no_black_tiles))
for i in range(0, 100):
    floor.iterate()
    if i < 10 or ((i + 1) % 10) == 0:
        print("Day {}: {}".format(i + 1, floor.no_black_tiles))
