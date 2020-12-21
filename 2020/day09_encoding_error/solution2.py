import itertools

f = open("input.txt", "r")
xmas_stream = [int(number) for number in f.readlines()]


def verify_number(number, preceeding_numbers):
    for combination in itertools.permutations(preceeding_numbers, 2):
        if sum(combination) == number:
            return True
    return False


def verify_stream(stream):
    for n in range(25, len(stream)):  # first 25 numbers are pre-amble
        if verify_number(number=stream[n], preceeding_numbers=stream[n - 25:n]) is False:
            return stream[n]
    return True


def sub_arrays(array):
    for sub_array_width in range(1, len(array)):
        for sub_array_start in range(len(array) - sub_array_width + 1):
            yield array[sub_array_start:sub_array_start + sub_array_width]


def find_weakness(stream, invalid_number):
    fault_position = stream.index(invalid_number)
    search_space = stream[:fault_position]
    for sub_array in sub_arrays(search_space):
        if sum(sub_array) == invalid_number:
            # Return the sum of the first and last item in the sorted list.
            return sum(sorted(sub_array)[::len(sub_array) - 1])
    return None


stream_faulty_number = verify_stream(xmas_stream)
if stream_faulty_number is not True:
    print("Faulty number is: {}".format(stream_faulty_number))
    weakness = find_weakness(xmas_stream, stream_faulty_number)
    if weakness is not None:
        print("The weakness is: {}".format(weakness))
    else:
        print("Weakness not found...")
else:
    print("Stream is valid!")
