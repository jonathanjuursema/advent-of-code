f = open("input.txt", "r")
depths = [int(depth) for depth in f.readlines()]

increases = 0
for start_of_window in range(len(depths)):
    if start_of_window < 2:
        # The first window ends at the third item in the list (index 2).
        continue

    # Take a slice of all measurements that corresponds to the "current" window.
    # In Python, the last item in a slice is not inclusive,
    # so we do +1 to add the "current" item to the current window as well.
    current_window = depths[start_of_window - 2:start_of_window + 1]

    # This is just a sequential number to identify the window in the output cosmetically.
    window_number = start_of_window - 1

    if start_of_window == 2:
        # The first window does not have a previous window to compare to.
        print("{}: {} (N/A - no previous sum)".format(window_number, sum(current_window)))
        continue

    # Take a slice one position further back to get the previous window.
    previous_window = depths[start_of_window - 3:start_of_window]

    does_increase = sum(current_window) > sum(previous_window)

    print("{}: {} ({}rease)".format(window_number, sum(current_window), "inc" if does_increase else "no inc"))

    if does_increase:
        increases += 1

print("=============================================")
print("Measured depth is bigger for {} measurement windows.".format(increases))
