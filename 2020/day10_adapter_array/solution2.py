import time


f = open("input.txt", "r")
all_adapters = [int(adapter) for adapter in f.readlines()]

all_adapters = sorted(all_adapters)
all_adapters.insert(0, 0)  # The outlet in the seat.
all_adapters.append(all_adapters[-1] + 3)  # The built-in adapter of the device.

paths = {}
for joltage in all_adapters:
    paths[joltage] = 1 if joltage == 0 else 0

start_time = time.time()
# Hadn't figured this non-recursive solution out myself. Thanks to colleagues and Reddit for hints.
for adapter, joltage in enumerate(all_adapters):
    continue_looking = True
    next_adapter = adapter + 1
    current_paths = paths[joltage]
    while continue_looking and next_adapter < len(all_adapters):
        next_joltage = all_adapters[next_adapter]
        if next_joltage - joltage <= 3:
            paths[next_joltage] += current_paths
            next_adapter += 1
        else:
            continue_looking = False
print("--- %s seconds ---" % (time.time() - start_time))

print("There are {} possible arrangements.".format(
    paths[all_adapters[-1]]))

