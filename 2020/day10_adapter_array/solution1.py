f = open("input.txt", "r")
adapters = [int(adapter) for adapter in f.readlines()]

adapters = sorted(adapters)
adapters.insert(0, 0)  # The outlet in the seat.
adapters.append(adapters[-1] + 3)  # The built-in adapter of the device.

joltage_differences = {}

for n in range(1, len(adapters) - 1):  # We can skip the seat adapter and device adapter. Won't take those ones out.
    joltage_difference = adapters[n] - adapters[n - 1]
    if joltage_difference <= 0:
        print("These are the same joltages! (n={})".format(n))
    if joltage_difference > 3:
        print("These adapters are not compatible! (n={})".format(n))

    if joltage_difference not in joltage_differences.keys():
        joltage_differences[joltage_difference] = 0
    joltage_differences[joltage_difference] += 1

print("Joltage distribution is {}*1, {}*3, answer: {}".format(
    joltage_differences[1],
    joltage_differences[3],
    joltage_differences[1] * joltage_differences[3]
))
