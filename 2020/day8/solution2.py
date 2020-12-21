f = open("input.txt", "r")
original_program = f.readlines()


# Returns a tuple of (next operation, change to accumulator)
def execute_instruction(program, operation_position):
    instruction = program[operation_position].split(" ")
    if instruction[0] == "nop":
        return operation_position + 1, 0
    if instruction[0] == "acc":
        return operation_position + 1, int(instruction[1])
    if instruction[0] == "jmp":
        return operation_position + int(instruction[1]), 0
    else:
        raise ValueError("Instruction {} not recognized!".format(instruction[0]))


def evaluate_program(program):
    lines_executed = []
    accumulator = 0
    current_line = 0

    while True:
        lines_executed.append(current_line)
        next_line, d_accumulator = execute_instruction(program, current_line)
        accumulator += d_accumulator

        if next_line in lines_executed:
            return False  # Program stuck in loop.

        if next_line >= len(program):
            print("Program terminated gracefully. Accumulator is {}.".format(accumulator))
            return True  # Program did complete.

        current_line = next_line


# Test every line to see if we can change it, and if the resulting modified program works.
for line_number in range(0, len(original_program)):
    instruction = original_program[line_number].split(" ")
    modified_program = original_program.copy()
    if instruction[0] == "acc":
        continue  # We don't change acc's.
    elif instruction[0] == "nop":
        modified_program[line_number] = "jmp {}".format(instruction[1])
        result = evaluate_program(modified_program)
    elif instruction[0] == "jmp":
        modified_program[line_number] = "nop {}".format(instruction[1])
        result = evaluate_program(modified_program)
    else:
        raise ValueError("Instruction {} not recognized!".format(instruction[0]))

    if result is True:
        print("Found it! Changed line: {} (+1)".format(line_number))
        break