f = open("input.txt", "r")
instructions = f.readlines()

lines_executed = []
accumulator = 0
current_line = 0


# Returns a tuple of (next operation, change to accumulator)
def execute_instruction(operation_position):
    instruction = instructions[operation_position].split(" ")
    if instruction[0] == "nop":
        return operation_position + 1, 0
    if instruction[0] == "acc":
        return operation_position + 1, int(instruction[1])
    if instruction[0] == "jmp":
        return operation_position + int(instruction[1]), 0
    else:
        raise ValueError("Instruction {} not recognized!".format(instruction[0]))


while True:
    lines_executed.append(current_line)
    next_line, d_accumulator = execute_instruction(current_line)
    accumulator += d_accumulator

    # The termination condition, if we re-visit an already executed line, we've found the loop!
    if next_line in lines_executed:
        print("Line {} is going to be executed twice! Previous line is {}, value of accumulator is {}.".format(
            next_line, current_line, accumulator))
        break

    current_line = next_line
