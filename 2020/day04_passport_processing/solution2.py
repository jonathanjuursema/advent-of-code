import jsonschema
import yaml

f = open("input.txt", "r")
batch = f.read()

# Split batch in passports (on 2 newlines)
passports = batch.strip().split("\n\n")
# Reformat all passports to seperate all fields on space and not some on newline
passports = [p.replace("\n", " ") for p in passports]


# Takes space seperated fields and builds a dictionary.
def format_passport(passport):
    dictionary = {}
    number_fields = ['byr', 'iyr', 'eyr']
    fields = passport.split(" ")
    for field in fields:
        data = field.split(":")
        dictionary[data[0]] = int(data[1]) if data[0] in number_fields else data[1]
    return dictionary


passports = [format_passport(p) for p in passports]

schema_file = open("schema.yaml", "r")
schema = yaml.load(schema_file, Loader=yaml.FullLoader)

valid_passports = []
for passport in passports:
    try:
        jsonschema.validate(instance=passport, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print("Invalid passport:\n{}\n{}\n\n".format(passport, err))
        continue
    valid_passports.append(passport)

print("Encountered {} valid passports!".format(len(valid_passports)))
