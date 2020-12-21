f = open("test.txt", "r")
notes = f.readlines()


class Bus:
    def __init__(self, id, offset):
        self._id = int(id)
        self._offset = int(offset)

    @property
    def id(self):
        return self._id

    @property
    def offset(self):
        return self._offset


busses = [Bus(id, index) for index, id in enumerate(notes[1].split(",")) if id != "x"]


# Although I had an exhaustive search algorithm that would work for the smaller test samples, it was too inefficient
# to work for the larger input. I've pieced together this code by taking someone else's and searching for hints on
# Reddit to figure out WHY it works and rewriting the other code to be more readable.
# - https://github.com/MJK88/adventofcode
# - https://www.reddit.com/r/adventofcode/comments/kc60ri/2020_day_13_can_anyone_give_me_a_hint_for_part_2/
# This is also a very good thread:
# - https://www.reddit.com/r/adventofcode/comments/kcb3bb/2020_day_13_part_2_can_anyone_tell_my_why_this/
def find_common_time(busses_subset):
    start_time = busses_subset[0].id  # This is the first moment the first bus matches again.
    time_delta = start_time  # For the first bus, we can expect the bus to match every $bus.id time.
    print("Matched bus {} on t={}, new interval is {}".format(busses_subset[0].id, start_time, time_delta))

    t = start_time
    for bus in busses_subset[1:]:  # We already have the first bus, only need to check the others.
        # This time matches (per the "rules") if the time + the offset of the bus in the list
        # (the bus must leave at x subsequent minutes where x is the offset (or the position in
        # the list in the notes)) modulo the bus ID (the bus leaves every $bus_id minutes) equals zero.
        # The module saves is from having to check which "loop" of the bus this is.
        while not (t + bus.offset) % bus.id == 0:
            t += time_delta

        # Since we know the bus numbers are prime, we can expect the match interval to be
        # multiples of this bus id multiplied by the previous one.
        time_delta *= bus.id
        print("Matched bus {} on t={}, new interval is {}".format(bus.id, t, time_delta))

    return t


common_t = find_common_time(busses)
print("Common T is t={}".format(common_t))
