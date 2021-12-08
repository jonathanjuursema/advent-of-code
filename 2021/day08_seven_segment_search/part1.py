f = open("input.txt", "r")

digit_count = 0

for line in f.readlines():

    # For part 1, we're only interested in the latter part of the input.
    notes = line.strip("\n").split(" | ")
    output = notes[1]

    # Loop over all output digits.
    for digit in output.split(" "):
        if len(digit) in [2, 3, 4, 7]:
            digit_count += 1

print("There are {} digits in the output that are either 1, 4, 7 or 8.".format(digit_count))