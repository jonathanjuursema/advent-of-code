f = open("input.txt", "r")


class Octopi:
    _octopi = None
    _x_len = 0
    _y_len = 0
    _flashes = 0

    def __init__(self, puzzle_input):
        self._octopi = []
        for row in puzzle_input.split("\n"):
            self._octopi.append([int(octopus) for octopus in row.strip("\n")])
        self._x_len = len(self._octopi[0])
        self._y_len = len(self._octopi)

    def __str__(self):
        lines = []
        for row in self._octopi:
            lines.append("".join(["{}".format(octopus) if octopus < 10 else "0" for octopus in row]))
        return "\n".join(lines)

    def step(self):
        # Create a new state based on the old one.
        new_octopi = [row[:] for row in self._octopi]

        # Increase all energy levels by one.
        for y in range(0, self._y_len):
            for x in range(0, self._x_len):
                self._octopi[y][x] += 1

        # Flash!
        while self._are_yet_to_flash():
            for y in range(0, self._y_len):
                for x in range(0, self._x_len):
                    # This octopus has already flashed. It deserves some rest.
                    if self._octopi[y][x] == 0:
                        continue
                    # This octopus can flash!
                    if self._octopi[y][x] == 10:
                        # Smile!
                        self._octopi[y][x] = 0
                        self._flashes += 1
                        # Increase the energy level of nearby octopi.
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:

                                # Skip the current octopus.
                                if dx == 0 and dy == 0:
                                    continue

                                # Don't forget this...
                                nx = x + dx
                                ny = y + dy

                                # Skip octopi that don't exist.
                                if nx < 0 or ny < 0 or nx >= self._x_len or ny >= self._y_len:
                                    continue

                                # Skip neighbours that have already flashed (0).
                                # Skip neighbours that are already ready to flash (10).
                                # These will flash in the next iteration of this function (but still in the same step).
                                if self._octopi[ny][nx] in [0, 10]:
                                    continue

                                self._octopi[ny][nx] += 1

    # Helper function to determine if there are still octopi that can flash.
    def _are_yet_to_flash(self):
        for y in range(0, self._y_len):
            for x in range(0, self._x_len):
                if self._octopi[y][x] == 10:
                    return True
        return False

    # How many flashes have there been?
    def flashes(self):
        return self._flashes

    # Are the octopi flashing in sync?
    def in_sync(self):
        for y in range(0, self._y_len):
            for x in range(0, self._x_len):
                if self._octopi[y][x] != 0:
                    return False
        return True


octopi = Octopi(f.read())

# print("Before any steps:")
# print(octopi)
# print("")


step = 0
while octopi.in_sync() is False:
    step += 1
    octopi.step()
    # print("After step {}:".format(step))
    # print(octopi)
    # print("")
    if step in [10, 100]:
        print("Observed {} flashes after step {}.".format(octopi.flashes(), step))

print("The octopi are flashing in sync after step {}!".format(step))
