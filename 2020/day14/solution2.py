f = open("input.txt", "r")
instructions = f.readlines()


class Program:

    def __init__(self):
        self._mask = "0" * 36
        self._memory = {}

    def _update_mask(self, mask):
        self._mask = mask

    def _update_memory(self, location, integer):
        addresses = self._explode_memory_addresses(location)
        for address in addresses:
            self._memory[address] = integer

    def _explode_memory_addresses(self, address):
        address_mask = self._apply_mask_to_integer(address)
        return Program.explode_memory_addresses_recursive([address_mask])

    @staticmethod
    def explode_memory_addresses_recursive(addresses):
        i = addresses[0].find("X")
        if i < 0:
            return addresses
        new_addresses = []
        for address in addresses:
            new_addresses.append(address[:i] + '1' + address[i + 1:])
            new_addresses.append(address[:i] + '0' + address[i + 1:])
        return Program.explode_memory_addresses_recursive(new_addresses)

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
            [Program.apply_mask_to_singly_bit(original_bit=bitstring[i], mask_bit=self._mask[i]) for i in
             range(0, len(bitstring))])
        # Convert the string representation of a binary value back to an integer.
        return masked_bitstring

    @staticmethod
    def apply_mask_to_singly_bit(original_bit, mask_bit):
        if mask_bit == "X":
            return "X"
        elif mask_bit == "1":
            return "1"
        elif mask_bit == "0":
            return original_bit
        else:
            raise ValueError("Unexpected mask bit: {}".format(mask_bit))

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
