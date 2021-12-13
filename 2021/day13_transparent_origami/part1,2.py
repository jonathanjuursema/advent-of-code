f = open("input.txt", "r")


class Paper:
    _dots = []
    _instructions = []

    _max_x = 0
    _max_y = 0

    def __init__(self, lines):
        coordinates = []
        for line in [l.strip("\n") for l in lines]:
            if line == "":
                continue

            # We're reading the folding instructions and saving them.
            if line.startswith("fold along "):
                instruction = line.replace("fold along ", "").strip("\n").split("=")
                axis = instruction[0]
                position = int(instruction[1])
                self._instructions.append((axis, position))

            # We're reading coordinates and saving them.
            else:
                coordinate = [int(c) for c in line.split(",")]
                coordinates.append(coordinate)
                self._max_x = max(self._max_x, coordinate[0])
                self._max_y = max(self._max_y, coordinate[1])

        self._dots = coordinates

    # This function prints the matrix by mapping all the points on a matrix.
    def __str__(self):
        print_dots = [[0] * (self._max_x + 1) for _ in range(self._max_y + 1)]

        for coordinate in self._dots:
            print_dots[coordinate[1]][coordinate[0]] = 1

        lines = []
        for line in print_dots:
            lines.append("".join(["#" if c == 1 else "." for c in line]))
        return "\n".join(lines)

    # This function will do all the folds.
    def fold(self):
        first = True
        for instruction in self._instructions:
            self._do_fold(instruction)
            # We need to know the amount of dots after the first fold for part 1.
            if first:
                print("After the first fold there are {} dots.".format(self.no_dots))
                first = False

    # This function does only one fold.
    def _do_fold(self, instruction):
        # First, according to the instructions, we'll have to fold the paper over an axis.
        # This means that over that axis we loose half of the length.
        if instruction[0] == 'y':
            self._max_y //= 2
        elif instruction[0] == 'x':
            self._max_x //= 2

        new_dots = []
        # For each dot...
        for dot in self._dots:
            new_dot = dot
            axis = 1 if instruction[0] == 'y' else 0
            # Verify if, for the axis we're interested in for this instruction, that point is beyond the folding line.
            if new_dot[axis] > instruction[1]:
                # If it is, we "mirror" it over the folding line. We do this by calculating
                # 1) how many "positions" it is beyond the folding line
                # 2) removing that amount twice (once to put it "on" the folding line, once to put it back on the
                #    paper in the mirrored position
                new_dot[axis] = new_dot[axis] - 2 * (new_dot[axis] - instruction[1])
            new_dots.append(new_dot)

        self._dots = new_dots

    @property
    # Note that this code does not remove duplicate dots. Therefore the easiest way to count the number of dots is
    # to just print the output and calculate how many '#'s there are. This automatically takes part of the
    # deduplication. Sorry, I'm lazy today.
    def no_dots(self):
        return "{}".format(self).count("#")


paper = Paper(f.readlines())
paper.fold()

print("\nThis is wat the paper reads:\n{}".format(paper))
