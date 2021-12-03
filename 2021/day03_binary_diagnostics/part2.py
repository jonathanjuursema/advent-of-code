f = open("input.txt", "r")
binary_values = [str(binary).strip("\n") for binary in f.readlines()]

binary_length = len(binary_values[0])  # Take one value to determine the length (example and input are different).


def find_value(binary_values, algo):
    print("Determining {}...".format(algo))
    diagnostics_value = ""
    # Loop over all positions in the binary values, starting at the first.
    i = 0
    # STOP if we are left with only 1 binary value.
    while i in range(binary_length) and len(binary_values) > 1:

        # Determine the most common bit for that position in each binary value.
        number_of_1_bits = 0
        for binary_value in binary_values:
            if binary_value[i] == "1":
                number_of_1_bits += 1

        if algo == "oxygen_generator":
            bit_to_keep = "1" if number_of_1_bits >= len(binary_values) / 2 else "0"
        elif algo == "co2_scrubber":
            bit_to_keep = "1" if number_of_1_bits < len(binary_values) / 2 else "0"

        # Now we know what numbers we need to keep, based on the start of the value.
        # Assemble a new list of binary values for the next iteration.
        diagnostics_value += bit_to_keep
        binary_values = [binary_value for binary_value in binary_values if
                         binary_value.startswith(diagnostics_value)]

        print("Preferred bit in position {} is {}, keeping {} entries.".format(i + 1, bit_to_keep, len(binary_values)))

        i += 1

    # If we are left with only one value, that value is the one we are looking for.
    return binary_values[0]


oxygen_generator_rating = find_value(binary_values=binary_values, algo="oxygen_generator")
# int(string, base) converts a number in a specific base to another base.
# In this case from base 2 (binary) to base 10 (decimal)
print("Oxygen Generator Rating is {} (binary) or {} (decimal)".format(oxygen_generator_rating,
                                                                      int(oxygen_generator_rating, 2)))

co2_scrubber_rating = find_value(binary_values=binary_values, algo="co2_scrubber")
print("CO2 Scrubber Rating is {} (binary) or {} (decimal)".format(co2_scrubber_rating, int(co2_scrubber_rating, 2)))

print("Puzzle answer is {}".format(int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)))
