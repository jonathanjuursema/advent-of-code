f = open("input.txt", "r")

ERROR_SCORE_LOOKUP = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
REPAIR_SCORE_LOOKUP = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

CHUNK_OPENS = ['(', '[', '{', '<']
CHUNK_CLOSES = [')', ']', '}', '>']


def analyze_line(line, repair=False):
    expected_closings = []
    for character in line:
        if character in CHUNK_OPENS:
            expected_closings.append(CHUNK_CLOSES[CHUNK_OPENS.index(character)])
        elif character in CHUNK_CLOSES:
            expected_closing = expected_closings.pop(-1)
            if expected_closing != character:
                print("Expected {}, but found {} instead.".format(expected_closing, character))
                return ERROR_SCORE_LOOKUP[character]

    # The line is at least not corrupt. Only continue if we want to repair the line.
    if repair is False:
        return 0

    # Start the repair. We know exactly what to expect, it's in `expected_closings`. We can complete the line by
    # reversing the array and appending it at the end.
    expected_closings = reversed(expected_closings)

    repair_score = 0
    for character in expected_closings:
        repair_score *= 5
        repair_score += REPAIR_SCORE_LOOKUP[character]

    print("Line can be repaired by adding {} (score: {})".format("".join(expected_closings), repair_score))

    return repair_score


cleaned_program = []
program_score = 0
for line in [l.strip("\n") for l in f.readlines()]:
    line_score = analyze_line(line)
    if line_score > 0:
        program_score += line_score
    else:
        cleaned_program.append(line)

print("High score! You have achieved a syntax error score of: {}".format(program_score))
print("Continuing with cleaned program...")

program_scores = []
for line in cleaned_program:
    line_score = analyze_line(line, repair=True)
    program_scores.append(line_score)

program_scores = sorted(program_scores)

print("Repair complete! Middle repair score: {}".format(program_scores[len(program_scores) // 2]))
