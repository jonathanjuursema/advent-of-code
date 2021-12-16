f = open("input.txt", "r")
lines = f.read().split("\n")

template = lines[0]
template = [polymer for polymer in template]

# In a huge surprise to noone the solution of part 1 didn't scale for part 2. So we needed an approach similar to the
# lanternfish of an earlier puzzle. We don't care about the exact polymer, we only want to keep track of how often
# polymers occur. To do this, we keep track of all polymer duo's.

# Construct the insertion rules again.
insertion_rules = {}
for line in lines[2:]:
    rule = line.split(" -> ")
    insertion_rules[rule[0]] = rule[1]

print("Making polymer")


# We need this function twice, so let's split it out. :)
# From the combination rules we can construct a dict of all possible combinations and initialize the count to 0.
def make_empty_counts_dict(rules):
    counts = {}
    for polymer_combination in rules.keys():
        counts[polymer_combination] = 0
    return counts


# Loop over the initial template and count all polymer duo's.
combination_counts = make_empty_counts_dict(insertion_rules)
for i in range(0, len(template) - 1):
    combination = "{}{}".format(template[i], template[i + 1])
    combination_counts[combination] += 1

# Now we're going to do the 40 iterations.
for step in range(0, 40):
    # Make a new counting structure.
    new_combination_counts = make_empty_counts_dict(insertion_rules)
    # We initialize this as 1 and not 0 because we use the "number of duos" as the length of the chain.
    # A chain of 5 polymers consists of 4 duos. Write it down on paper and it makes sense.
    new_template_length = 1

    # Loop over the previous counting structure. For each polymer duo, find the two resulting duo's.
    # For example, a CH duo, results in a CB and BH duo due to the combination rules. This also works for amounts.
    # For example, 5 CB duos result in 5 CH and 5 HB duos.
    # Add these to the counting structure.
    for combination, count in combination_counts.items():
        if count == 0:
            continue
        inserted_polymer = insertion_rules[combination]
        new_polymers = [
            "{}{}".format(combination[0], inserted_polymer),
            "{}{}".format(inserted_polymer, combination[1])
        ]
        for new_polymer in new_polymers:
            new_combination_counts[new_polymer] += count
            new_template_length += count

    # Print the length.
    print("Step {}: length {}".format(step + 1, new_template_length))
    combination_counts = new_combination_counts

print("Polymer complete!")

# Now we do the same counting trick as with part 1 but with a catch. Since there is no string to loop over we do it
# differently. For every combination, we only take the last polymer and add that polymer count to the total for that
# polymer. The first polymer of that combination will be counted when counting the other combinations.
# If we do this consistently (always take the last polymer), we get to the correct result. We only need to *also* count
# the first polymer of *only* the first combination.
quantities = {}
first = True
for combination, count in combination_counts.items():
    polymer = combination[1]
    if polymer not in quantities.keys():
        quantities[polymer] = 0
    quantities[polymer] += count
    if first:
        first = False
        polymer = combination[0]
        if polymer not in quantities.keys():
            quantities[polymer] = 0

min_q = None
max_q = None

for polymer in quantities.keys():
    quantity = quantities[polymer]
    if min_q is None or min_q[0] > quantity:
        min_q = (quantity, polymer)
    if max_q is None or max_q[0] < quantity:
        max_q = (quantity, polymer)

print("Most common: {} ({})".format(max_q[1], max_q[0]))
print("Least common: {} ({})".format(min_q[1], min_q[0]))
print("Difference: {}".format(max_q[0] - min_q[0]))
