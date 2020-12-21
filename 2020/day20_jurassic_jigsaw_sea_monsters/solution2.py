import numpy
import math

f = open("input.txt", "r")
input_images = f.read().split("\n\n")


class Image:

    def __init__(self, input):
        input_lines = input.splitlines()
        self._tile_no = int((input_lines.pop(0)).replace("Tile ", "").replace(":", ""))
        self._tile_array = numpy.array([list(line) for line in input_lines])
        self._size = len(self._tile_array)
        self._fixed = None

    @property
    def string(self):
        lines = []
        for line in range(0, self._size):
            lines.append("".join(self.data_row(line)))
        return "\n".join(lines)

    @property
    def no(self):
        return self._tile_no

    @property
    def data(self):
        return numpy.copy(self._tile_array)

    @property
    def size(self):
        return self._size

    def data_row(self, row_no):
        return self._tile_array[row_no, :]

    def get_position(self):
        return self._fixed

    def set_position(self, position):
        if self._fixed is None:
            self._fixed = position
        else:
            raise Exception('Can\'t change position for fixed image {}!'.format(self.no))

    @property
    def has_position(self):
        return self._fixed is not None

    def search_for_monster(self):
        monster_pattern = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]
        monsters = 0
        for y in range(0, self._size - 2):  # We don't have to look in the last two rows. The monster won't fit.
            for x in range(0, self._size - 19):  # Same goes for the last nineteen columns.
                area_can_have_monster = True
                for n in range(0, 3):
                    if area_can_have_monster is not True:
                        break
                    image_line = self.data_row(y + n)
                    for m in range(0, 20):
                        if monster_pattern[n][m] == '#':
                            if image_line[x + m] != '#':
                                area_can_have_monster = False
                                break
                if area_can_have_monster:
                    monsters += 1
        return monsters

    def rotate(self, k):
        if self.has_position:
            raise Exception('Cannot rotate {} anymore. It is fixed!'.format(self.no))
        self._tile_array = numpy.rot90(self._tile_array, k=k)

    def flip(self, axis):
        if self.has_position:
            raise Exception('Cannot flip {} anymore. It is fixed!'.format(self.no))
        self._tile_array = numpy.flip(self._tile_array, axis=axis)

    # Do the comparison with one orientation of the other image.
    def _test_with_image(self, image):
        image_data = image.data
        pos = self.get_position()
        # Top of this matches bottom of other.
        if (self._tile_array[0, :] == image_data[-1, :]).all():
            image.set_position((pos[0], pos[1] - 1))
            return True
        # Top of other matches bottom of this.
        elif (image_data[0, :] == self._tile_array[-1, :]).all():
            image.set_position((pos[0], pos[1] + 1))
            return True
        # Left of this matches right of other.
        elif (self._tile_array[:, 0] == image_data[:, -1]).all():
            image.set_position((pos[0] - 1, pos[1]))
            return True
        # Right of this matches left of other.
        elif (image_data[:, 0] == self._tile_array[:, -1]).all():
            image.set_position((pos[0] + 1, pos[1]))
            return True

    # Iterate over the orientations of the other image. With each orientation, test.
    def _find_match_with_image(self, image):
        if self.no == image.no:
            return
        if self._test_with_image(image):
            return
        if image.has_position:
            return
        for rotate in range(0, 4):
            image.rotate(k=1)
            if self._test_with_image(image):
                return
            for flip in [0, 1, 0, 1]:
                image.flip(axis=flip)
                if self._test_with_image(image):
                    return

    def find_matches_in_images(self, list_of_images):
        for image in list_of_images:
            if image.has_position:
                continue
            self._find_match_with_image(image)


# Do the combining thing. This function returns the grid, and the top_left coordinate in a tuple.
def combine_images_to_grid(raw_images):
    images = []
    for input_image in raw_images:
        images.append(Image(input_image))

    # Do all the matching.
    images[0].set_position((0, 0))
    all_have_match = False
    while all_have_match == False:
        print("Matching interation...")
        all_have_match = True
        for image in images:
            if image.has_position is True:
                image.find_matches_in_images(images)
            else:
                all_have_match = False

    # Find top-left.
    top_left = (len(images), len(images))
    grid = {}
    for image in images:
        i_pos = image.get_position()
        if i_pos[0] < top_left[0]:
            top_left = (i_pos[0], top_left[1])
        if i_pos[1] < top_left[1]:
            top_left = (top_left[0], i_pos[1])
        grid["{}_{}".format(i_pos[0], i_pos[1])] = image

    return grid, top_left


# Make composite grid image.
def make_composite(top_left, image_grid):
    axis_length = int(math.sqrt(len(image_grid.keys())))
    no_lines = image_grid["{}_{}".format(top_left[0], top_left[1])].size
    composite_lines = ["Tile 0:"]  # Image header. We con't care about the number but now we can re-use the Image class.
    for y in range(top_left[1], top_left[1] + axis_length):
        for row_no in range(1, no_lines - 1):  # Skip the first and last line (those are only for matching).
            row = ""
            for x in range(top_left[0], top_left[0] + axis_length):
                row += "".join(image_grid["{}_{}".format(x, y)].data_row(row_no)[1:-1])  # Skip first and last again.
            composite_lines.append(row)
    return Image("\n".join(composite_lines))


image_grid, top_left_coordinate = combine_images_to_grid(raw_images=input_images)
composite_image = make_composite(image_grid=image_grid, top_left=top_left_coordinate)
print("Composite image done!")

monsters = 0
for rotate in range(0, 4):
    composite_image.rotate(k=1)
    for flip in [0, 1, 0, 1]:
        composite_image.flip(axis=flip)
        n = composite_image.search_for_monster()
        if n > 0:
            if monsters != 0 and monsters != n:
                raise Exception("Found value that seems off...")
            monsters = n

print("Found {} monsters.".format(monsters))
roughness = composite_image.string.count('#') - (15 * monsters)  # There are 15 #'s in a monster.
print("Roughness of the waters is {}.".format(roughness))
