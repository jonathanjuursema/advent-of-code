import re

f = open("input.txt", "r")
input = f.read().split("\n\n")
input_rules = input[0]
input_messages = input[1].splitlines()


# From: https://stackoverflow.com/a/22389330/7316014
def set_list(l, i, v):
    try:
        l[i] = v
    except IndexError:
        for _ in range(i - len(l) + 1):
            l.append(None)
        l[i] = v


def assemble_rules(raw_rules):
    rule_data = []
    regex_sub_rule_simple = r"([0-9]+): ([0-9\s]+)"
    regex_sub_rule_multi = r"([0-9]+): ([0-9\s\|]+)"
    regex_character = r"([0-9]+): \"([a-z]+)\""
    for line in raw_rules.splitlines():
        if "\"" in line:
            rule_info = re.match(regex_character, line)
            set_list(rule_data, int(rule_info.group(1)), rule_info.group(2))
        elif "|" in line:
            rule_info = re.match(regex_sub_rule_multi, line)
            rule_no = int(rule_info.group(1))
            groups = rule_info.group(2).split(" | ")
            data = []
            for group in groups:
                data.append([int(n) for n in group.split(" ")])
            set_list(rule_data, rule_no, data)
        else:
            rule_info = re.match(regex_sub_rule_simple, line)
            rule_no = int(rule_info.group(1))
            data = [int(n) for n in rule_info.group(2).split(" ")]
            set_list(rule_data, rule_no, data)
    return rule_data


def generate_regex(rule_set, rule_no, regex=""):
    this_rule_data = rule_set[rule_no]

    if type(this_rule_data) is str:
        return regex + this_rule_data

    elif type(this_rule_data) is list:

        # This is the simple type.
        if type(this_rule_data[0]) is int:
            # For each item in the list, get the required regex match, and make it so they need to appear after each
            # other.
            for sub_rule_no in this_rule_data:
                regex = generate_regex(rule_set=rule_set, rule_no=sub_rule_no, regex=regex)
                pass
            return regex

        # This is the "or" type.
        if type(this_rule_data[0]) is list:
            # For each alternative, make the regex. Then combine them using an "or".
            alternatives = []
            for sub_rule_set in this_rule_data:
                sub_regex = ""
                for sub_rule_no in sub_rule_set:
                    sub_regex = generate_regex(rule_set=rule_set, rule_no=sub_rule_no, regex=sub_regex)
                alternatives.append(sub_regex)
            return regex + "({})".format("|".join(alternatives))


assembled_rule_data = assemble_rules(input_rules)
pattern = re.compile("{}".format(generate_regex(rule_set=assembled_rule_data, rule_no=0)))
print("Regex: {}".format(pattern))
count = 0
for message in input_messages:
    m = pattern.fullmatch(message)
    if m:
        count += 1
print("{} messages match!".format(count))
