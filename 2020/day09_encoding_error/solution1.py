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
            print("Number {} doesn't match protocol!".format(stream[n]))
            return False
    return True


verify_stream(xmas_stream)
