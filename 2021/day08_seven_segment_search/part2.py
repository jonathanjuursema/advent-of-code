f = open("input.txt", "r")

ALL_SIGNAL_WIRES = "abcdefg"


# For main program scroll alllll the way down.
# This is a helpful function to make sure digit wire information is always sorted to it can be compared.
def sort_config(digit_string):
    characters = [char for char in digit_string]
    return "".join(sorted(characters))


# Look-up table for wire configurations including some helper functions.
class DigitLut:
    _lut_dict = None

    def __init__(self):
        self._lut_dict = [None] * 10

    def add_config(self, wire_config, digit):
        self._lut_dict[digit] = sort_config(wire_config)

    def digit_to_config(self, digit):
        return self._lut_dict[digit]

    def config_to_digit(self, config):
        config = sort_config(config)
        for digit in range(0, 10):
            if self._lut_dict[digit] == config:
                return digit
        return None

    def config_known(self, config):
        for digit in range(0, 10):
            if self._lut_dict[digit] == sort_config(config):
                return True
        return False

    def decipher(self, input):
        output = ""
        for input_digit in input.split(" "):
            output += str(self.config_to_digit(config=input_digit))
        return int(output)


# The algorithm to figure out what configuration maps to what digit.
def analyze_configurations(configuration):
    digit_lut = DigitLut()

    configurations = configuration.split(" ")

    # First, we write down the digits that are immediately obvious.
    for digit_config in configurations:

        if len(digit_config) == 2:
            digit_lut.add_config(wire_config=digit_config, digit=1)
        elif len(digit_config) == 4:
            digit_lut.add_config(wire_config=digit_config, digit=4)
        elif len(digit_config) == 3:
            digit_lut.add_config(wire_config=digit_config, digit=7)
        elif len(digit_config) == 7:
            digit_lut.add_config(wire_config=digit_config, digit=8)

    # Armed with this, we can try to figure out more.

    for digit_config in configurations:
        # We can use a trick for the 6 and 0 (both 6 wires).
        if len(digit_config) == 6:
            # Figure out the missing signal wire.
            for w in ALL_SIGNAL_WIRES:
                # Found the missing signal wire.
                if w not in digit_config:
                    # If the missing wire IS present in the 1, we've found our 6.
                    if w in digit_lut.digit_to_config(1):
                        digit_lut.add_config(wire_config=digit_config, digit=6)
                    # If the missing wire IS present in the 4 but not in the 1, we've found the 0.
                    elif w in digit_lut.digit_to_config(4) and w not in digit_lut.digit_to_config(1):
                        digit_lut.add_config(wire_config=digit_config, digit=0)

        # We can also use a trick for the 3 and 2 (5 wires).
        if len(digit_config) == 5:
            # For the 3, we have to check if all wires for the 1 are also present in the wire configuration.
            # This is not the case for 2 and 5.
            if all(w in digit_config for w in digit_lut.digit_to_config(1)):
                digit_lut.add_config(wire_config=digit_config, digit=3)

            # For the 2, we have to check if all MISSING wires ARE present in the 4.
            # This is not the case for 3 and 5.
            # Figure out the missing wires.
            else:
                missing_wires = ""
                for w in ALL_SIGNAL_WIRES:
                    if w not in digit_config:
                        missing_wires += w
                if all(w in digit_lut.digit_to_config(4) for w in missing_wires):
                    digit_lut.add_config(wire_config=digit_config, digit=2)

    # We now have 0, 1, 2, 3, 4, 6, 7 and 8. Only missing the 5 and the 9.
    for digit_config in configurations:
        # The 5 is the only 5-wire configuration that is not known yet.
        # The 9 is the only 6-wire configuration that is not known yet.
        if digit_lut.config_known(digit_config) is False:
            if len(digit_config) == 5:
                digit_lut.add_config(wire_config=digit_config, digit=5)
            elif len(digit_config) == 6:
                digit_lut.add_config(wire_config=digit_config, digit=9)

    # And we're done! Return the look-up table.
    return digit_lut


# Main program.
output_sum = 0

for line in [l.strip("\n") for l in f.readlines()]:
    notes = line.strip("\n").split(" | ")
    configuration = notes[0]
    output = notes[1]

    digit_lut = analyze_configurations(configuration=configuration)
    deciphered_output = digit_lut.decipher(input=output)
    output_sum += deciphered_output
    print("{}: {}".format(output, deciphered_output))

print("Sum: {}".format(output_sum))
