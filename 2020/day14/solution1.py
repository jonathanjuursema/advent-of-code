f = open("input.txt", "r")
instructions = f.readlines()


class Program:

    def __init__(self):
        self._mask = "0" * 36
        self._memory = {}

    def _update_mask(self, mask):
        self._mask = mask

    def _update_memory(self, location, integer):
        self._memory[location] = self._apply_mask_to_integer(integer)

    # Convert an integer into a string representation of the binary value.
    @staticmethod
    def integer_to_bitstring(integer):
        return "{0:b}".format(integer)

    # Apply the mask to the integer.
    def _apply_mask_to_integer(self, integer):
        # Also left pad the string representation with "0" to make it the same length as the mask.
        bitstring = Program.integer_to_bitstring(integer).rjust(len(self._mask), "0")
        # For each position in the bitstring, take the input for X's, or the mask for other values.
        masked_bitstring = "".join(
            [bitstring[i] if self._mask[i] == "X" else self._mask[i] for i in range(0, len(bitstring))])
        # Convert the string representation of a binary value back to an integer.
        return int(masked_bitstring, 2)

    def parse_instruction(self, instruction):
        task = instruction.strip().split(" = ")
        if task[0] == "mask":
            self._update_mask(task[1])
        elif task[0].startswith("mem"):
            self._update_memory(location=int(task[0].replace("mem[", "").replace("]", "")), integer=int(task[1]))
        else:
            raise ValueError("Unrecognized instruction:\n\t{}".format(instruction))

    @property
    def memory_value(self):
        return sum(self._memory.values())


program = Program()
for instruction in instructions:
    program.parse_instruction(instruction)

print("Sum of all values in memory: {}".format(program.memory_value))
