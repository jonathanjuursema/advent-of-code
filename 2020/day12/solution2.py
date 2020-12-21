import math

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
        self._waypoint = (10, -1)

    @property
    def position(self):
        return self._position

    def execute_instruction(self, instruction):
        action, amount = instruction[0], int(instruction[1:])
        if action in ["L", "R"]:
            self._turn_waypoint(amount * (1 if action == "R" else -1))
        elif action in ["N", "S", "E", "W"]:
            self._move_waypoint(amount, self._movement_map[action])
        elif action == "F":
            self._move_ship_to_waypoint(amount)
        else:
            raise ValueError("Unrecognized instruction: {}".format(instruction))

    def _turn_waypoint(self, degrees):
        radians = math.radians(degrees)
        self._waypoint = (
            int(math.cos(radians) * self._waypoint[0]) - int(math.sin(radians) * self._waypoint[1]),
            int(math.cos(radians) * self._waypoint[1]) + int(math.sin(radians) * self._waypoint[0])
        )

    def _move_waypoint(self, amount, direction):
        self._waypoint = (
            self._waypoint[0] + (amount * direction[0]),
            self._waypoint[1] + (amount * direction[1])
        )

    def _move_ship_to_waypoint(self, times):
        self._position = (
            self._position[0] + (times * self._waypoint[0]),
            self._position[1] + (times * self._waypoint[1])
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
