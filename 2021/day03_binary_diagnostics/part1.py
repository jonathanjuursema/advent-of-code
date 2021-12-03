f = open("input.txt", "r")
binary_values = [str(binary).strip("\n") for binary in f.readlines()]

binary_length = len(binary_values[0])  # Take one value to determine the length (example and input are different).
number_of_values = len(binary_values)  # Number of "entries" in the list of binary values.

# For each position in the binary number, keep track of how many of the observed values is a 1.
bits_that_are_1 = [0] * binary_length

for binary_value in binary_values:  # Loop over all values
    for i in range(binary_length):  # Loop over each bit in the value
        if binary_value[i] == "1":
            bits_that_are_1[i] += 1

gamma_rate = ""
epsilon_rate = ""
for i in range(binary_length):
    # If the number of observed ones is more than half the number of values, 1 is the most common value. Otherwise 0.
    # Note this leaves the case of an equal nubmer of 1's and 0's out of consideration.
    most_common_bit = "1" if bits_that_are_1[i] > (number_of_values / 2) else "0"
    least_common_bit = "1" if most_common_bit == "0" else "0"
    print("Most common bit in position {} is {}".format(i + 1, most_common_bit))

    # Append most common bit to gamma rate binary value, and least common bit to epsilon rate binary value.
    gamma_rate += most_common_bit
    epsilon_rate += least_common_bit

# int(string, base) converts a number in a specific base to another base.
# In this case from base 2 (binary) to base 10 (decimal)
print("Gamma rate is {} (binary) or {} (decimal)".format(gamma_rate, int(gamma_rate, 2)))
print("Epsilon rate is {} (binary) or {} (decimal)".format(epsilon_rate, int(epsilon_rate, 2)))

print("Puzzle answer is {}".format(int(gamma_rate, 2) * int(epsilon_rate, 2)))
