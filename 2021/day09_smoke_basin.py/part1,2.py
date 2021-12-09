from math import prod

f = open("input.txt", "r")
height_data = f.readlines()

height_map = []

for line in height_data:
    height_map.append([int(height) for height in line.strip("\n")])

map_len_x = len(height_map[0])
map_len_y = len(height_map)

basins = []
risk_level_sum = 0


def calculate_basin_size(height_map, basin_locations, x, y):
    height = height_map[y][x]

    for neighbour in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx = x + neighbour[0]
        ny = y + neighbour[1]

        # This neighbour is already in the basin:
        if (nx, ny) in basin_locations:
            continue

        # The edge points have fewer neighbours.
        if nx < 0 or nx >= map_len_x or ny < 0 or ny >= map_len_y:
            continue

        neighbour_height = height_map[ny][nx]
        if neighbour_height == 9:
            # Locations with height 9 are never part of the basin.
            continue
        elif neighbour_height > height:
            # Locations with a height strictly higher than the current height are part of the basin.
            basin_locations.append((nx, ny))
            # Find basin locations adjecent to this neighbour.
            basin_locations = calculate_basin_size(height_map=height_map, basin_locations=basin_locations, x=nx, y=ny)

    return basin_locations


for x in range(0, map_len_x):
    for y in range(0, map_len_y):
        # For each height...
        height = height_map[y][x]

        # A point with height 9 will never be a high point.
        if height == 9:
            continue

        is_low_point = True

        # Check all four neighbours:
        for neighbour in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + neighbour[0]
            ny = y + neighbour[1]

            # The edge points have fewer neighbours.
            if nx < 0 or nx >= map_len_x or ny < 0 or ny >= map_len_y:
                continue

            # If the neighbour is lower or equal in height, this point will not be the lowest point in the area.
            neighbour_height = height_map[ny][nx]
            if neighbour_height <= height:
                is_low_point = False
                break

        # If the point is a low point, calculate risk level and add it to the total.
        if is_low_point:
            risk_level = 1 + height
            risk_level_sum += risk_level

            # If this is a low point, calculate the size of the basin around it.
            # For this, we write a recursive function that checks all neighbours,
            # and make sure that a specific location is not added to the basin twice.
            basin_locations = [(x, y)]
            basin_locations = calculate_basin_size(height_map=height_map, basin_locations=basin_locations, x=x, y=y)
            basins.append(basin_locations)

print("The sum of risk levels of the area is: {}".format(risk_level_sum))
print("There are {} basins.".format(len(basins)))

basin_sizes = [len(basin) for basin in basins]
basin_sizes = sorted(basin_sizes, reverse=True)

print("The product of the largest 3 basins is: {}".format(prod(basin_sizes[:3])))
