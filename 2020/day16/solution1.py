import re

f = open("input.txt", "r")
input = f.read().split("\n\n")

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

nearby_tickets = [[int(value) for value in ticket.split(",")] for ticket in input[2].splitlines() if
                  not ticket.startswith("nearby")]

error_rate = 0

for ticket in nearby_tickets:
    for value in ticket:
        valid = False
        for field in field_values.keys():
            if field_values[field]['from_1'] <= value <= field_values[field]['to_1']:
                valid = True
                continue
            if field_values[field]['from_2'] <= value <= field_values[field]['to_2']:
                valid = True
                continue
        if valid is False:
            error_rate += value

print("Error rate: {}".format(error_rate))
