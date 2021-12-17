from math import inf

f = open("input.txt", "r")
transmission = f.read().strip("\n")


class PacketDecoder:
    _version = None
    _type_id = None
    _literal_value = None
    _sub_packets = []
    _length_id = None

    _bits = None
    _discarded_bits = None

    @staticmethod
    def bits_to_int(bit_string):
        number = 0
        bit = 1
        for i in range(len(bit_string) - 1, -1, -1):
            if bit_string[i] == "1":
                number += bit
            bit *= 2
        return number

    @staticmethod
    def hex_to_bits(hex_string):
        convert_dict = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110",
                        "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101",
                        "E": "1110", "F": "1111"}
        bit_string = ""
        for char in hex_string:
            bit_string += convert_dict[char]
        return bit_string

    def __init__(self, transmission_bits):
        self._version = PacketDecoder.bits_to_int(transmission_bits[:3])
        self._type_id = PacketDecoder.bits_to_int(transmission_bits[3:6])

        self._sub_packets = []
        self._literal_value = None
        self._length_id = None

        self._bits = None
        self._discarded_bits = None

        # Literal Value
        if self._type_id == 4:
            number_bits = ""
            start_pos = 6
            while True:
                number_bits += transmission_bits[start_pos + 1:start_pos + 5]
                if transmission_bits[start_pos] == "0":
                    break
                start_pos += 5
            self._literal_value = PacketDecoder.bits_to_int(number_bits)
            self._discarded_bits = transmission_bits[start_pos + 5:]
            if all([c == "0" for c in self._discarded_bits]):
                self._discarded_bits = None
            self._bits = transmission_bits[:start_pos + 5]

        # Operator Packet
        else:
            self._length_id = int(transmission_bits[6])

            # Length is 15-bit number indicating the number of bits for the sub-packets.
            if self._length_id == 0:
                length = PacketDecoder.bits_to_int(transmission_bits[7:22])
                payload_start = 22
                while (payload_start - 22) < length:
                    packet = PacketDecoder(transmission_bits[payload_start:])
                    payload_start += len(packet.bits)
                    self._sub_packets.append(packet)

                self._discarded_bits = transmission_bits[payload_start:]
                if all([c == "0" for c in self._discarded_bits]):
                    self._discarded_bits = None
                self._bits = transmission_bits[:payload_start]

            # Length is 11-bit number indicating the number of sub-packets.
            else:
                length = PacketDecoder.bits_to_int(transmission_bits[7:18])
                payload_start = 18
                while len(self._sub_packets) < length:
                    packet = PacketDecoder(transmission_bits[payload_start:])
                    self._sub_packets.append(packet)
                    payload_start += len(packet.bits)

                self._discarded_bits = transmission_bits[payload_start:]
                if all([c == "0" for c in self._discarded_bits]):
                    self._discarded_bits = None
                self._bits = transmission_bits[:payload_start]

    @property
    def remaining_bits(self):
        return self._discarded_bits

    @property
    def bits(self):
        return self._bits

    @property
    def version_number_sum(self):
        version_sum = self._version
        for sub_packet in self._sub_packets:
            version_sum += sub_packet.version_number_sum
        return version_sum

    @property
    def value(self):
        # Sum packet
        if self._type_id == 0:
            value = 0
            for sub_packet in self._sub_packets:
                value += sub_packet.value
            return value
        # Product packet
        elif self._type_id == 1:
            value = self._sub_packets[0].value
            for i in range(1, len(self._sub_packets)):
                value *= self._sub_packets[i].value
            return value
        # Minimum packet
        elif self._type_id == 2:
            value = inf
            for sub_packet in self._sub_packets:
                value = min(value, sub_packet.value)
            return value
        # Maximum packet
        elif self._type_id == 3:
            value = -inf
            for sub_packet in self._sub_packets:
                value = max(value, sub_packet.value)
            return value
        # Literal value
        elif self._type_id == 4:
            return self._literal_value
        # Greater than packet
        elif self._type_id == 5:
            return int(self._sub_packets[0].value > self._sub_packets[1].value)
        # Less than packet
        elif self._type_id == 6:
            return int(self._sub_packets[0].value < self._sub_packets[1].value)
        # Equal packet
        elif self._type_id == 7:
            return int(self._sub_packets[0].value == self._sub_packets[1].value)


transmission = PacketDecoder(transmission_bits=PacketDecoder.hex_to_bits(transmission))

print("Sum of versions: {}".format(transmission.version_number_sum))
print("Transmission value: {}".format(transmission.value))
