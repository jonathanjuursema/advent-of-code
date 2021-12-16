f = open("input.txt", "r")
lines = f.read().split("\n")

template = lines[0]
template = [polymer for polymer in template]

# Read and parse the polymerisation rules. It's a two-layer dictionary that takes in the first polymer, the second
# polymer and returns the polymer that should go in between.
insertion_rules = {}
for line in lines[2:]:
    polymers = [p for p in line.replace(" -> ", "")]
    if polymers[0] not in insertion_rules.keys():
        insertion_rules[polymers[0]] = {}
    insertion_rules[polymers[0]][polymers[1]] = polymers[2]

# Perform the 10 steps requested for part 1.
for step in range(0, 10):
    # Build an entirely new template.
    new_template = []
    # Loop over every polymer duo.
    for i in range(0, len(template) - 1):
        # Append the left-most polymer.
        new_template.append(template[i])
        # Find the polymer that goes in between and append it.
        if template[i] in insertion_rules.keys():
            if template[i + 1] in insertion_rules[template[i]].keys():
                new_template.append(insertion_rules[template[i]][template[i + 1]])
        # The right-most polymer gets appended in the next step.
    # And finally append the last polymer as well because it is left out in the last step
    new_template.append(template[-1])

    # Set the current template as the new template.
    template = new_template
    print("Step {}: length {}".format(step + 1, len(template)))

print("Polymer complete!")

# Construct a dict that contains the
quantities = {}
for polymer in template:
    if polymer not in quantities.keys():
        quantities[polymer] = 0
    quantities[polymer] += 1

# Find the most and least common polymers.
min_q = None
max_q = None

for polymer in quantities.keys():
    quantity = quantities[polymer]
    if min_q is None or min_q[0] > quantity:
        min_q = (quantity, polymer)
    if max_q is None or max_q[0] < quantity:
        max_q = (quantity, polymer)

# And done!
print("Most common: {} ({})".format(max_q[1], max_q[0]))
print("Least common: {} ({})".format(min_q[1], min_q[0]))
print("Difference: {}".format(max_q[0] - min_q[0]))
