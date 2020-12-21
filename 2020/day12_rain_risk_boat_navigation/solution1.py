f = open("input.txt", "r")
instructions = f.readlines()


class Ship:
    _movement_map = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    _direction_map = {
        0: 'N',
        90: 'E',
        180: 'S',
        270: 'W'
    }

    def __init__(self):
        self._position = (0, 0)
        self._orientation = 90

    @property
    def position(self):
        return self._position

    def execute_instruction(self, instruction):
        action, amount = instruction[0], int(instruction[1:])
        if action in ["L", "R"]:
            self._turn(amount * (1 if action == "R" else -1))
        elif action in ["N", "S", "E", "W", "F"]:
            if action == "F":
                action = self._deg_to_dir(self._orientation)
            self._move(amount, self._movement_map[action])
        else:
            raise ValueError("Unrecognized instruction: {}".format(instruction))

    def _turn(self, degrees):
        self._orientation = (self._orientation + degrees) % 360

    def _move(self, amount, direction):
        self._position = (
            self._position[0] + (amount * direction[0]),
            self._position[1] + (amount * direction[1])
        )

    def _deg_to_dir(self, degrees):
        try:
            return self._direction_map[degrees]
        except:
            raise ValueError("Unsupported number of degrees: {}".format(degrees))

    def _dir_to_deg(self, direction):
        return self._direction_map.keys()[self._direction_map.values().index(direction)]

    @property
    def manhattan_distance(self):
        return abs(self._position[0]) + abs(self._position[1])


ship = Ship()
for instruction in instructions:
    ship.execute_instruction(instruction)
print("The ship travelled {}.".format(ship.manhattan_distance))
