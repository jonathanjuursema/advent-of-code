f = open("input.txt", "r")
batch = f.read()

# Split batch in passports (on 2 newlines)
passports = batch.strip().split("\n\n")
# Reformat all passports to seperate all fields on space and not some on newline
passports = [p.replace("\n", " ") for p in passports]


# Takes space seperated fields and builds a dictionary.
def format_passport(passport):
    dictionary = {}
    fields = passport.split(" ")
    for field in fields:
        data = field.split(":")
        dictionary[data[0]] = data[1]
    return dictionary


passports = [format_passport(p) for p in passports]

required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

valid_passports = []
for passport in passports:
    found_keys = set(passport.keys())
    if len(required_keys - found_keys) == 0:
        valid_passports.append(passport)

print("Encountered {} valid passports!".format(len(valid_passports)))
