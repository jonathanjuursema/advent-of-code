f = open("input.txt", "r")
boarding_passes = f.read().splitlines()


def decode_boarding_pass(boarding_pass):
    row = range(0, 128)
    column = range(0, 8)

    # Get column, these are the first seven characters. Remember: zero-index.
    for char in range(0, 7):
        if boarding_pass[char] == "F":
            row = row[:len(row) // 2]
        elif boarding_pass[char] == "B":
            row = row[len(row) // 2:]
        else:
            raise Exception("Unexpected character in code {}: {}".format(boarding_pass, char))

    # Get row, these are the last three characters. Remember: zero-index.
    for char in range(7, 10):
        if boarding_pass[char] == "L":
            column = column[:len(column) // 2]
        elif boarding_pass[char] == "R":
            column = column[len(column) // 2:]
        else:
            raise Exception("Unexpected character in code {}: {}".format(boarding_pass, char))

    return row[0], column[0], row[0] * 8 + column[0]  # row, column, seat id


all_seat_ids = set(range(0, 8 * 128))

for boarding_pass in boarding_passes:
    row, column, seat_id = decode_boarding_pass(boarding_pass)
    all_seat_ids.remove(seat_id)

# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
last_seat_id = 0
for seat_id in all_seat_ids:
    if seat_id > last_seat_id + 1:
        print("Your seat id: {}".format(seat_id))
        break
    last_seat_id = seat_id
