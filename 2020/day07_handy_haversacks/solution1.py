import re

f = open("input.txt", "r")
raw_rules = f.readlines()
parsed_rules = {}


def parse_rule(raw_rule):
    if "no other" not in raw_rule:
        # Because regexes can't capture repeating groups, we first have to know how many groups to expect:
        # Source: https://stackoverflow.com/questions/37003623/how-to-capture-multiple-repeated-groups
        n_of_subbags = raw_rule.count(",") + 1
        # Now we write a regex to parse the rules, appending the sub-bag regex n times.
        regex = r"([a-z\s]+) bags contain {}\.".format("".join([r"([0-9]+) ([a-z\s]+) bags?,?\s?"] * n_of_subbags))
    else:
        regex = r"([a-z\s]+) bags contain no other bags\."
    # We now have a list of structured matches: bag color, 1st sub-bag amount, 1st sub-bag color, 2nd sub-bag amount,
    # 2nd sub-bag color, etc.
    rule_match = re.match(regex, raw_rule)
    return rule_match.groups()


# Returns a tuple of color, dict_with_subbags
def structure_rule(rule_data):
    n_of_subbags = len(rule_data) // 2
    if n_of_subbags == 0:
        return rule_data[0], None
    else:
        color = rule_data[0]
        n = 1
        data_dict = {}
        while n < n_of_subbags * 2:
            sub_count = rule_data[n]
            sub_color = rule_data[n + 1]
            data_dict[sub_color] = int(sub_count)
            n += 2
        return color, data_dict


# Find all bag colors contained within a specific color bag.
def find_all_sub_colors(top_color, rule_dict):
    sub_colors = []
    # For that top color, check what color of bags can be contained in that top bag.
    if rule_dict[top_color] is not None:
        for sub_color in rule_dict[top_color].keys():
            # And append that color to the list.
            sub_colors.append(sub_color)
            # For each sub color bag, check if that bag can contain additional colors.
            if rule_dict[top_color][sub_color] is not None:
                for sub_sub_color in find_all_sub_colors(sub_color, rule_dict):
                    # And append these colors to the list as well.
                    sub_colors.append(sub_sub_color)

    # We cast to set to de-duplicate colors.
    return set(sub_colors)


rule_dict = {}
for raw_rule in raw_rules:
    rule_data = parse_rule(raw_rule)
    color, contents = structure_rule(rule_data)
    rule_dict[color] = contents

possible_bags = []
for outer_bag_color in rule_dict.keys():
    if 'shiny gold' in find_all_sub_colors(outer_bag_color, rule_dict):
        possible_bags.append(outer_bag_color)

print("{} bag colors can carry the shiny gold bag.".format(len(possible_bags)))
