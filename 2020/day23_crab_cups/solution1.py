from collections import deque

f = open("input.txt", "r")
cup_labels = [int(l) for l in list(f.read().replace("\n", ""))]


class Game:

    def __init__(self, starting_cup_labels, n_rounds):
        self._current_cup_labels = starting_cup_labels
        self._n_rounds = n_rounds
        self._round_no = 1
        self._selected_cup = self._current_cup_labels[0]
        self._min_value = min(self._current_cup_labels)
        self._max_value = max(self._current_cup_labels)

    def execute(self, debug=False):
        while self._round_no <= self._n_rounds:
            if debug:
                print("-- move {} --".format(self._round_no))
                print("cups: {}".format(" ".join("({})".format(c) if c == self._selected_cup else str(c)
                                                 for c in self._current_cup_labels)))
            picked_up_cups = []
            cur_cup_index = self._current_cup_labels.index(self._selected_cup)

            # Pick up the three cups to the right of the selected cup.
            for p in range(1, 4):
                picked_up_cups.append(self._current_cup_labels[(cur_cup_index + p) % len(self._current_cup_labels)])
            for c in picked_up_cups:
                self._current_cup_labels.remove(c)
            if debug:
                print("pick up: {}".format(picked_up_cups))

            # Select the destination cup.
            destination_cup = self._selected_cup - 1
            while destination_cup not in self._current_cup_labels:
                if destination_cup < self._min_value:
                    destination_cup = self._max_value
                else:
                    destination_cup -= 1
            if debug:
                print("destination: {}\n".format(destination_cup))
            dest_cup_index = self._current_cup_labels.index(destination_cup)

            # Insert the picked up cups back.
            # Reversed because inserting into a list shifts all elements to the right.
            for el in reversed(picked_up_cups):
                self._current_cup_labels.insert(dest_cup_index + 1, el)

            # Update variables for next round
            cur_cup_index = self._current_cup_labels.index(self._selected_cup)
            self._selected_cup = self._current_cup_labels[(cur_cup_index + 1) % len(self._current_cup_labels)]
            self._round_no += 1
            pass

        print("Cups after game: {}".format(self._current_cup_labels))

        # List shifting from: https://stackoverflow.com/a/2150125
        items = deque(self._current_cup_labels)
        while items[0] != 1:
            items.rotate(-1)

        print("Puzzle answer: {}".format("".join(str(c) for c in list(items)[1:])))


game = Game(starting_cup_labels=cup_labels, n_rounds=100)
game.execute()
