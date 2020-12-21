f = open("input.txt", "r")
puzzle_input = f.read()

raw_groups = puzzle_input.split("\n\n")
groups = []

sum_counts = 0

for raw_group in raw_groups:
    # ever answer per member as a list item
    group_answers = raw_group.split("\n")
    # make every person's answer a set
    group_answers = [set(l) for l in group_answers]

    # find the intersection of all sets in a group - e.g. answers that are in all groups
    group_answers_all_yes = set.intersection(*group_answers)

    sum_counts += len(group_answers_all_yes)

print("Total numbers of common 'yes' per group: {}".format(sum_counts))
