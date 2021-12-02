f = open("input.txt", "r")
instructions = f.readlines()

aim = 0
pos_forward = 0
pos_depth = 0

for instruction in instructions:

    instruction_parts = instruction.split(" ")
    direction = instruction_parts[0]
    amount = int(instruction_parts[1])

    if direction == "forward":
        pos_forward += amount
        pos_depth += (aim * amount)

    elif direction == "down":
        aim += amount

    elif direction == "up":
        aim -= amount

    else:
        print("Unknown instruction: {}".format(instruction))
        break

print("We've arrived at position {} at depth {}.".format(pos_forward, pos_depth))
print("Puzzle answer: {}".format(pos_forward * pos_depth))
