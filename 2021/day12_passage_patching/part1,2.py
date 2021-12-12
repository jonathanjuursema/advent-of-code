f = open("input.txt", "r")


class Cave:
    _neighbours = []
    _name = None

    def __init__(self, name):
        self._neighbours = []
        self._name = name

    def add_neighbour(self, neighbour):
        self._neighbours.append(neighbour)

    def get_neighbours(self):
        return self._neighbours

    def get_name(self):
        return self._name


class CaveSystem:
    _start = None
    _all_caves = []
    _all_cave_names = []
    _routes = []
    _small_cave_visits = None

    def __init__(self, small_cave_visits=1):
        self._start = None
        self._all_caves = []
        self._all_cave_names = []
        self._routes = []
        self._small_cave_visits = small_cave_visits

    def __str__(self):
        lines = []
        for route in self._routes:
            lines.append(",".join([cave.get_name() for cave in route]))
        return "\n".join(sorted(lines))

    def no_routes(self):
        return len(self._routes)

    def explore(self):
        self._routes = self._continue_route(base_route=[self._start])

    def _continue_route(self, base_route):
        # If the last visited cave is end, and the route has not been discarded, it is finished and can be returned.
        last_cave = base_route[-1]
        if last_cave.get_name() == 'end':
            return [base_route]

        routes = []

        next_caves = last_cave.get_neighbours()
        for next_cave in next_caves:
            # We can't revisit start...
            if next_cave.get_name() == 'start':
                continue

            route = [cave for cave in base_route]
            route.append(next_cave)
            # Is this route still valid? If not, discard this route.
            route_valid = True
            # A small cave can only be visited a certain number of times.
            caves_visited = {}
            for cave in route:
                if cave.get_name() not in caves_visited.keys():
                    caves_visited[cave.get_name()] = 0
                caves_visited[cave.get_name()] += 1

            if self._small_cave_visits == 1:
                # All small caves can only be visited once.
                for cave_name in caves_visited.keys():
                    if cave_name.islower() and caves_visited[cave_name] > 1:
                        route_valid = False
                        break
            elif self._small_cave_visits == 2:
                # ONE small cave van be visited twice, the rest only once.
                two_visits = False
                for cave_name in caves_visited.keys():
                    if cave_name.islower() and caves_visited[cave_name] > 2:
                        route_valid = False
                        break
                    elif cave_name.islower() and caves_visited[cave_name] == 2:
                        if two_visits is False:
                            two_visits = True
                            continue
                        route_valid = False
                        break

            if route_valid is True:
                routes.extend(self._continue_route(base_route=route))
        return routes

    def add_connection(self, cave_names):
        # Make sure all caves exist.
        for cave_name in cave_names:
            if cave_name not in self._all_cave_names:
                cave = Cave(cave_name)
                self._all_caves.append(cave)
                self._all_cave_names.append(cave_name)
                if cave_name == 'start':
                    self._start = cave

        # Connect the caves.
        cave_1 = self._get_cave(cave_names[0])
        cave_2 = self._get_cave(cave_names[1])
        cave_1.add_neighbour(cave_2)
        cave_2.add_neighbour(cave_1)

    def _get_cave(self, cave_name):
        for cave in self._all_caves:
            if cave.get_name() == cave_name:
                return cave
        return None


cave_systems = {
    'pt1': CaveSystem(),
    'pt2': CaveSystem(small_cave_visits=2)
}

for connection in f.readlines():
    caves = connection.strip("\n").split("-")
    for cave_system in cave_systems.values():
        cave_system.add_connection(caves)

for cave_system_name in cave_systems.keys():
    print("Exploring {}...".format(cave_system_name))
    cave_systems[cave_system_name].explore()
    # print("{}".format(cave_systems[cave_system_name]))
    print("...contains {} routes.".format(cave_systems[cave_system_name].no_routes()))
