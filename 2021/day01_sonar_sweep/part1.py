f = open("input.txt", "r")
depths = [int(depth) for depth in f.readlines()]

increases = 0
for i in range(len(depths)):
    does_increase = False
    if i == 0:
        print("{} (N/A - no previous measurement)".format(depths[i]))
        continue  # Skip the first measurement because there is no previous measurement to compare.
    else:
        does_increase = depths[i] > depths[i - 1]

    print("{} ({}rease)".format(depths[i], "inc" if does_increase else "no inc"))

    if does_increase:
        increases += 1

print("=============================================")
print("Measured depth is bigger for {} measurements.".format(increases))
