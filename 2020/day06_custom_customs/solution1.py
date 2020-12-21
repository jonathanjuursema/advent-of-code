f = open("input.txt", "r")
puzzle_input = f.read()

raw_groups = puzzle_input.split("\n\n")
groups = []

sum_counts = 0

for raw_group in raw_groups:
    # just put all answers from a group on one line
    group_answers = raw_group.replace("\n", "")
    # set(group_answers) makes a list of all answers an de-duplicates duplicate ones
    group_answers = set(group_answers)

    sum_counts += len(group_answers)

print("Total numbers of 'yes' per group: {}".format(sum_counts))
