import math

f = open("input.txt", "r")
notes = f.readlines()

arrival_time = int(notes[0])
busses = [int(id) for id in notes[1].split(",") if id != "x"]

earliest_departure = (None, None)
for bus_id in busses:
    iteration = math.floor(arrival_time / bus_id)
    next_departure = (bus_id * (iteration + 1)) - arrival_time
    if earliest_departure[1] is None or next_departure < earliest_departure[1]:
        earliest_departure = (bus_id, next_departure)

print("The earliest departure is bus {} in {} minutes. Puzzle answer: {}".format(earliest_departure[0],
                                                                                 earliest_departure[1],
                                                                                 earliest_departure[0] *
                                                                                 earliest_departure[1]))
