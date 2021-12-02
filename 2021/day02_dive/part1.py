f = open("input.txt", "r")
instructions = f.readlines()

pos_forward = 0
pos_depth = 0

for instruction in instructions:

    instruction_parts = instruction.split(" ")
    direction = instruction_parts[0]
    distance = int(instruction_parts[1])

    if direction == "forward":
        pos_forward += distance

    elif direction == "down":
        pos_depth += distance

    elif direction == "up":
        pos_depth -= distance

    else:
        print("Unknown instruction: {}".format(instruction))
        break

print("We've arrived at position {} at depth {}.".format(pos_forward, pos_depth))
print("Puzzle answer: {}".format(pos_forward * pos_depth))
