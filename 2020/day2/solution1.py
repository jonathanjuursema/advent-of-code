import re

f = open("input.txt", "r")
passwords = f.readlines()

valid, invalid = 0, 0


def is_valid(password, reqchar, min, max):
    count = password.count(reqchar)
    return count >= min and count <= max


for password_entry in passwords:
    info = re.match(r"([0-9]+)\-([0-9]+) (.): (.+)", password_entry)
    min, max, reqchar, password = int(info.group(1)), int(info.group(2)), info.group(3), info.group(4)
    if is_valid(password, reqchar, min, max):
        valid += 1
    else:
        invalid += 1

print("Counted {} valid and {} invalid password.".format(valid, invalid))
