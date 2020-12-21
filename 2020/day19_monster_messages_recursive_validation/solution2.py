import re

f = open("input.txt", "r")
input = f.read().split("\n\n")
input_rules = input[0]
input_messages = input[1].splitlines()
longest_input_message = max(len(s) for s in input_messages)


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


# We need to cheat around the loops. Luckily, the changed rules are exactly the rules directly mentioned by rule 0
# (so they're the 'first'). Also both rules 8 and 11 are not referenced by other rules. So we can safely 'cheat' them.
# Without worrying by side effects.
# I didn't figure this out without help. I've used among others the following comments on Reddit:
# - https://www.reddit.com/r/adventofcode/comments/kg1mro/2020_day_19_solutions/ggcu9ie

# If we look at how rule 8 changed, it would just match any amount of occurrences of rule 42.
def make_rule_8(rule_set):
    return "{}+".format(generate_regex(rule_set=rule_set, rule_no=42))


# Rule 11 seems to repeat inwards. So 42 31 is ok, so is 42 42 31 31 and 42 42 42 31 31 31.
# We just need to make sure the amount of repeats for 42 and 31 is the same. For this we can
# write a loop that does this for an n that terminates at a reasonable value. Since a match is
# in the end just a character, we can assume that there will be no more repeats than the length
# of the longest input divided by 2 (because we match two sets: 42 and 31).
def make_rule_11(rule_set):
    regex_42 = generate_regex(rule_set=rule_set, rule_no=42)
    regex_31 = generate_regex(rule_set=rule_set, rule_no=31)
    options = []
    for n in range(1, longest_input_message // 2):
        options.append("({r42}{{{n}}}{r31}{{{n}}})".format(r42=regex_42, r31=regex_31, n=n))
    return "|".join(options)


assembled_rule_data = assemble_rules(input_rules)
regex = "({r8})({r11})".format(
    r8=make_rule_8(rule_set=assembled_rule_data),
    r11=make_rule_11(rule_set=assembled_rule_data))
print("Regex: {}".format(regex))
pattern = re.compile(regex)
count = 0
for message in input_messages:
    m = pattern.fullmatch(message)
    if m:
        count += 1
print("{} messages match!".format(count))
