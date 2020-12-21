import re

f = open("input.txt", "r")
input = f.read().split("\n\n")

# Parse the allowed number ranges for fields.
field_values = {}
value_regex = r"([a-z\s]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)"
for line in input[0].splitlines():
    line_info = re.match(value_regex, line).groups()
    field_values[line_info[0]] = {
        'from_1': int(line_info[1]),
        'to_1': int(line_info[2]),
        'from_2': int(line_info[3]),
        'to_2': int(line_info[4]),
    }

# Parse nearby tickets as list of field values (integers).
nearby_tickets = [[int(value) for value in ticket.split(",")] for ticket in input[2].splitlines() if
                  not ticket.startswith("nearby")]

# Parse our ticket as list of field values (integers).
our_ticket = [int(value) for value in input[1].splitlines()[1].split(",")]

# Collect valid tickets
valid_tickets = []
for ticket in nearby_tickets:
    ticket_valid = True
    for value in ticket:
        value_valid = False
        for field in field_values.keys():
            if field_values[field]['from_1'] <= value <= field_values[field]['to_1']:
                value_valid = True
                continue
            if field_values[field]['from_2'] <= value <= field_values[field]['to_2']:
                value_valid = True
                continue
        if value_valid is False:
            ticket_valid = False
    if ticket_valid is True:
        valid_tickets.append(ticket)

# We're gonna make a matrix that allows is to keep track of the following:
# For each field and each column on the ticket, we're going to keep track of whether that column could be valid for
# that field.
# If, on a valid ticket, we find a value that does not conform to the field restrictions as parsed earlier, we're going
# to mark that combination as not possible.
field_validity_matrix = {}
for field in field_values.keys():
    field_validity_matrix[field] = [True for i in range(0, len(valid_tickets[0]))]

for ticket in valid_tickets:
    for valid_field_index, valid_field_value in enumerate(ticket):
        for field_name in field_values.keys():
            for field_matrix_index, field_matrix_valid in enumerate(field_validity_matrix[field_name]):
                if field_matrix_valid is False:
                    continue
                if field_values[field_name]['from_1'] <= valid_field_value <= field_values[field_name]['to_1']:
                    continue
                if field_values[field_name]['from_2'] <= valid_field_value <= field_values[field_name]['to_2']:
                    continue
                field_validity_matrix[field_name][valid_field_index] = False

# Now we have a matrix, but we still have some colums that could be used for multiple fields.
# We don't wanna resolve this manually, so we're going to "fix" combinations one by one, eliminating that field and
# column for other combinations. We should end up with a matrix where exactly one column matches exactly one field.

fixed_rows = set([])
while len(fixed_rows) != len(field_values.keys()):
    for field_name in field_values.keys():
        # This field is fixed (only one column can be used for this field) so we can invalidate this column for other
        # fields.
        if field_validity_matrix[field_name].count(True) == 1:
            fixed_column = field_validity_matrix[field_name].index(True)
            for invalidate_field_name in field_validity_matrix.keys():
                if invalidate_field_name == field_name:
                    continue
                field_validity_matrix[invalidate_field_name][fixed_column] = False
            fixed_rows.add(field_name)

puzzle_output = 1
# We're there!
print("Our ticket is as follows:")
for field_name in field_validity_matrix.keys():
    field_index = field_validity_matrix[field_name].index(True)
    print("{}: {}".format(field_name, our_ticket[field_index]))
    if field_name.startswith("departure"):
        puzzle_output *= our_ticket[field_index]

print("Puzzle output: {}".format(puzzle_output))
