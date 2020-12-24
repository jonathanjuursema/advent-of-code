from collections import deque

f = open("input.txt", "r")
cup_labels = [int(l) for l in list(f.read().replace("\n", ""))]


class Cup:

    def __init__(self, label):
        self.label = label

    def set_next(self, cup):
        self._next = cup

    @property
    def next(self):
        return self._next


class Game:

    def __init__(self, starting_cup_labels, n_rounds):
        _cups = []
        self._n_rounds = n_rounds
        self._round_no = 1

        # Make cups in a linked list.
        prev_cup = None
        for label in starting_cup_labels:
            cup = Cup(label=label)
            _cups.append(cup)
            if prev_cup is not None:
                prev_cup.set_next(cup)
            prev_cup = cup

        for label in range(10, 1000001):  # Range is not inclusive, but we need label 1000000.
            cup = Cup(label=label)
            _cups.append(cup)
            prev_cup.set_next(cup)
            prev_cup = cup

        # Link last to first cup.
        _cups[-1].set_next(_cups[0])

        self._selected_cup = _cups[0]
        self._cup_count = len(_cups)

        # Make look-up-list
        self._label_to_cups = [None] * (self._cup_count + 1)
        cup = self._selected_cup
        while self._label_to_cups[cup.label] is None:
            self._label_to_cups[cup.label] = cup
            cup = cup.next
        pass

    def print_cups(self):
        cups = []
        cup = self._selected_cup
        while cup.label not in cups:
            cups.append(cup.label)
            cup = cup.next
        print("cups: {}".format(" ".join("({})".format(c) if c == self._selected_cup.label else str(c)
                                         for c in cups)))

    def execute(self, debug=False):
        while self._round_no <= self._n_rounds:
            if debug:
                print("-- move {} --".format(self._round_no))
                self.print_cups()

            # Pick up the three cups to the right of the selected cup.
            picked_up_cup_labels = []
            pick_up_first = self._selected_cup.next
            cup_to_pick_up = pick_up_first
            for p in range(0, 3):
                picked_up_cup_labels.append(cup_to_pick_up.label)
                pick_up_last = cup_to_pick_up
                cup_to_pick_up = cup_to_pick_up.next
            if debug:
                print("pick up: {}".format(picked_up_cup_labels))

            # Select the destination cup.
            destination_cup_label = self._selected_cup.label - 1
            while True:
                if destination_cup_label <= 0:
                    destination_cup_label = self._cup_count
                elif destination_cup_label in picked_up_cup_labels:
                    destination_cup_label -= 1
                else:
                    break
            if debug:
                print("destination: {}\n".format(destination_cup_label))
            destination_cup = self._label_to_cups[destination_cup_label]

            # Insert the picked up cups back.
            self._selected_cup.set_next(pick_up_last.next)
            pick_up_last.set_next(destination_cup.next)
            destination_cup.set_next(pick_up_first)

            # Update variables for next round
            self._selected_cup = self._selected_cup.next
            self._round_no += 1
            pass

        cup_1 = self._label_to_cups[1].next
        cup_2 = cup_1.next
        print("Puzzle answer: {}".format(cup_1.label * cup_2.label))


print("Starting game...")
game = Game(starting_cup_labels=cup_labels, n_rounds=10000000)
game.execute()
