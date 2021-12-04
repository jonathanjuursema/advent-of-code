import numpy as np

f = open("input.txt", "r")
lines = [line.strip("\n") for line in f.readlines()]


class Board:
    _board = None
    id = None
    won = None

    # Initialize the board based on the input.
    def __init__(self, id, lines):
        # For reference.
        self.id = id
        # This one liner does the following. First it loops over every line.
        # For every line, it splits the string every 3 characters and converts that part to an integer.
        self._board = np.array([[line[i:i + 3].strip() for i in range(0, len(line), 3)] for line in lines])

        won = False

    # A number is called, search for it and tick it off.
    def call(self, number):
        # Tick off the number.
        self._board[self._board == number] = "X"

        # Check for a win.
        if self._check():
            self.won = True
            # If we win, calculate the score and return it.
            return self._score(last_called=number)
        # If we don't wint, return nothing.
        return None

    # Check for a win.
    def _check(self):
        # Check for all rows if all values are ticked off.
        for line in self._board:
            if all([cell == "X" for cell in line]):
                return True
        # Check for all columns if all values are ticked off.
        # `.T` transposes (flips) the axes of the board so we can now treat columns as rows.
        for column in self._board.T:
            if all([cell == "X" for cell in column]):
                return True
        return False

    # Calculate the score for a board.
    def _score(self, last_called):
        score = 0
        for line in self._board:
            for cell in line:
                if cell != "X":
                    score += int(cell)
        return score * int(last_called)


def play(numbers, boards):
    # Now let's play the game. Call each and every number until one board finishes.
    for number in numbers:
        print("Calling: {}".format(number))
        for board in boards:
            # If this board is already done, skip it.
            if board.won:
                continue
            # The call function returns True if the board wins. If the board wins, exit the loop.
            output = board.call(number)
            if output is not None:
                print("Board {} is done with score: {}".format(board.id, output))
                if all([board.won for board in boards]):
                    print("All boards are done!")
                    return


# Load the numbers to be called. Take the first line, split on the comma and convert to integers.
numbers = [number for number in lines[0].split(",")]

# Load the boards. The first board starts on line 3 (index: 2).
boards = []
l = 2
while l < len(lines):
    boards.append(Board(id=(l // 5) + 1, lines=lines[l:l + 5]))

    # All boards are five lines long, and are spaced by a newline. The next board starts 6 lines over.
    l += 6

play(numbers=numbers, boards=boards)
