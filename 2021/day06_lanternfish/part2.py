import numpy as np

f = open("input.txt", "r")

# So the solution to part 1 is not efficient enough for such a long timescale, but I was stuck on finding a way to stop
# simulating individual lanternfish. Luckily with a hint from my colleagues I got back on track.

# Let's not simulate all lanternfish. Every lanternfish with the same internal clock value is identical. For example, we
# know that 5 lanternfish with a clock of 4 result in 5 lanternfish with a clock of 3. And 100 lanternfish with a clock
# of 0 result in 100 lanternfish with a clock of 6 (the original lanternfish) and 100 lanternfish kids with a clock of
# 8. So let's just keep track of how many lanternfish we have with a specific internal clock.

# Make an array for all clock values 0 through 8. We have 0 lanternfish for every clock state.
lanternfish_with_state = [0]*9

# Add the initial lanternfish.
for initial_lanternfish in f.read().split(","):
    lanternfish_with_state[int(initial_lanternfish)] += 1

print("Initially: {} lanternfish ({})".format(sum(lanternfish_with_state), lanternfish_with_state))

for day in range(0, 256):
    # Let's remember how many lanternfish are giving birth today.
    parent_lanternfish = lanternfish_with_state[0]

    # Now we shift the array on position to the left. Remember: each lanternfish with clock 4 results in a lanternfish
    # with clock 3. lanternfish with a clock of 0 become a lanternfish with a clock of 6.
    # But wait, we're now making them lanternfish with a clock of 8? Well yes, but the 0-clock-lanternfish also create
    # an extra lanternfish with a clock of 8. Read on.
    lanternfish_with_state = np.roll(lanternfish_with_state, -1)

    # So as long as we add the lanternfish that gave birth back with clock 6, we're done!
    lanternfish_with_state[6] += parent_lanternfish

    print("After day {}: {} lanternfish ({})".format(day + 1, sum(lanternfish_with_state), lanternfish_with_state))