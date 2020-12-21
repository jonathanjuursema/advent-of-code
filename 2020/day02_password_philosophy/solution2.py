import re

f = open("input.txt", "r")
passwords = f.readlines()

valid, invalid = 0, 0


def is_valid(password, reqchar, pos1, pos2):
    # -1 because no "index zero"
    pos1_ok = password[pos1 - 1] == reqchar
    pos2_ok = password[pos2 - 1] == reqchar
    return pos1_ok ^ pos2_ok  # XOR, not OR


for password_entry in passwords:
    info = re.match(r"([0-9]+)\-([0-9]+) (.): (.+)", password_entry)
    pos1, pos2, reqchar, password = int(info.group(1)), int(info.group(2)), info.group(3), info.group(4)
    if is_valid(password, reqchar, pos1, pos2):
        valid += 1
    else:
        invalid += 1

print("Counted {} valid and {} invalid password.".format(valid, invalid))
