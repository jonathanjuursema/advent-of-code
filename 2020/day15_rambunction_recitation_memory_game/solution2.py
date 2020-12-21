f = open("input.txt", "r")
input = [int(i) for i in f.read().split(",")]


def determin_position_at(input_numbers, stop, print_steps=False):
    previous_number = input_numbers[0]
    seen = set([])
    last_turn_on_which_number_was_spoken = {}

    for i in range(0, stop):
        if i < len(input_numbers):
            number = input_numbers[i]
        else:
            if previous_number not in seen:
                number = 0
            else:
                number = i - 1 - last_turn_on_which_number_was_spoken[previous_number]

        if print_steps:
            print("Turn {:<4}: {}".format(i + 1, number))

        seen.add(previous_number)
        last_turn_on_which_number_was_spoken[previous_number] = i - 1
        previous_number = number
    return number


print(determin_position_at(input, 30000000))
