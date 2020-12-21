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


# Print entire grid.
def print_composite(top_left, image_grid):
    for y in range(top_left[1], top_left[1] + int(math.sqrt(len(images)))):
        for row_no in range(0, images[0].size):
            row = ""
            for x in range(top_left[0], top_left[0] + int(math.sqrt(len(images)))):
                row += "{} ".format("".join(grid["{}_{}".format(x, y)].data_row(row_no)))
            print(row)
        print("")


images = []
for input_image in input_images:
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

print("Combined image:\n")
print_composite(top_left=top_left, image_grid=grid)

print("Corner pieces:")
top_right = (top_left[0] + int(math.sqrt(len(images))) - 1, top_left[1])
bottom_left = (top_left[0], top_left[1] + int(math.sqrt(len(images))) - 1)
bottom_right = (top_right[0], bottom_left[1])

corner_values = []
corner_values.append(grid["{}_{}".format(top_left[0], top_left[1])].no)
corner_values.append(grid["{}_{}".format(top_right[0], top_right[1])].no)
corner_values.append(grid["{}_{}".format(bottom_left[0], bottom_left[1])].no)
corner_values.append(grid["{}_{}".format(bottom_right[0], bottom_right[1])].no)

print(corner_values)
print("Product: {}".format(numpy.prod(corner_values)))
