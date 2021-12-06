f = open("input.txt", "r")
lanternfish = [int(age) for age in f.read().split(",")]

print("Initial state: {}".format(lanternfish))

for day in range(0, 80):
    # First, all fish that are ready spawn a new fish.
    new_fish_count = sum([fish == 0 for fish in lanternfish])
    new_fish = [8] * new_fish_count

    # Then, update all the fish' timers.
    # Fish that have a timer bigger then 0 will have their timer reduced by one.
    # Fish that have a timer of 0 (and gave birth) will have their timer reset to 6.
    lanternfish = [fish - 1 if fish > 0 else 6 for fish in lanternfish]

    # Append the new fish to the school.
    lanternfish.extend(new_fish)

    print("After {} days: {}".format(day + 1, lanternfish))

print("There are now {} lanternfish.".format(len(lanternfish)))
