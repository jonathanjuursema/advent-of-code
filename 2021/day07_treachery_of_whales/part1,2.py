f = open("input.txt", "r")
initial_positions = [int(position) for position in f.read().strip("\n").split(",")]

minimum_fuel_part_1 = None
minimum_fuel_part_2 = None

# We try every position in the list of initial positions, no more. It wouldn't make sense to move all crabs to a point
# far away from where they currently are.
for target_position in range(min(initial_positions), max(initial_positions) + 1):
    # Here the fuel cost is literally the distance, so we can just sum all distances to get the total fuel cost.
    fuel_cost_part_1 = sum([abs(target_position - current_position) for current_position in initial_positions])
    if minimum_fuel_part_1 is None or fuel_cost_part_1 < minimum_fuel_part_1[0]:
        minimum_fuel_part_1 = (fuel_cost_part_1, target_position)

    # This is a little more tricky. I couldn't come up with a better approach than this, which is calculating the fuel
    # cost naively. Just solution finishes in just under 15 seconds on my machine. It's not very efficient.
    fuel_cost_part_2 = sum(
        [sum(range(0, abs(target_position - current_position) + 1)) for current_position in initial_positions])
    if minimum_fuel_part_2 is None or fuel_cost_part_2 < minimum_fuel_part_2[0]:
        minimum_fuel_part_2 = (fuel_cost_part_2, target_position)

    # The more performant approach is to use triangular numbers: https://en.wikipedia.org/wiki/Triangular_number
    # However, I did not know about this trick and was told about it by a friend later. Here's the more efficient
    # solution.
    # fuel_cost_part_2 = sum(
    #     [int(abs(target_position - current_position) * (abs(target_position - current_position) + 1) / 2)
    #      for current_position in initial_positions])
    # if minimum_fuel_part_2 is None or fuel_cost_part_2 < minimum_fuel_part_2[0]:
    #     minimum_fuel_part_2 = (fuel_cost_part_2, target_position)

print("[Pt.1] The smalles amount of fuel ({}) is spent for horizontal position {}.".format(minimum_fuel_part_1[0],
                                                                                           minimum_fuel_part_1[1]))
print("[Pt.2] The smalles amount of fuel ({}) is spent for horizontal position {}.".format(minimum_fuel_part_2[0],
                                                                                           minimum_fuel_part_2[1]))
