f = open("input.txt", "r")
lines = [line.replace(" ", "") for line in f.read().splitlines()]


def evaluate_expression(expression, debug=False):
    if debug:
        print("Solving: {}".format(expression))

    # Search for the multiplication operations from right to left. The priority is left to right which means we
    # first need the left hand side of an operation solved before we can solve the entire expression (see the example).
    mult_index = expression.rfind('*')

    plus_index = expression.find('+')
    left_par_index = expression.find('(')

    # We have no more operations to solve, just return the number.
    if plus_index == -1 and mult_index == -1 and left_par_index == -1:
        return int(expression)

    # We found a left-parenthesis! We'll need to find the matching right-parenthesis and evaluate the contents first...
    if left_par_index >= 0:
        depth = 0
        right_par_index = -1

        for i in range(left_par_index + 1, len(expression)):
            # If we encounter another left-parenthesis we simply ignore it for now (it will be resolved in the next
            # recursion) but make sure we increase the depth so we also ignore the next right-parenthesis!
            if expression[i] == '(':
                depth += 1
            elif expression[i] == ')' and depth > 0:
                depth -= 1
            elif expression[i] == ')' and depth == 0:
                right_par_index = i
                break

        if right_par_index >= 0:
            # Isolate the part in parenthesis.
            parts = [expression[:left_par_index], expression[left_par_index + 1:right_par_index],
                     expression[right_par_index + 1:]]

            # Solve the part in parenthesis.
            if debug:
                print("Resolving parenthesis part: {}".format(parts[1]))
            par_answer = evaluate_expression(parts[1], debug=debug)

            # Glue the expression back together.
            new_expression = "".join([parts[0], str(par_answer), parts[2]])
            return evaluate_expression(new_expression, debug=debug)

        raise ValueError("No closing parenthesis found in {}".format(expression))

    # We need to solve an addition operation. These take precedence over multiplication and require us to only multiply
    # the elements directly before and after the operation.
    elif plus_index >= 0:
        prev_operation_plus = expression[:plus_index].rfind('+')
        prev_operation_mult = expression[:plus_index].rfind('*')
        left_index = prev_operation_plus if prev_operation_plus > prev_operation_mult else prev_operation_mult

        next_operation_plus = expression[plus_index + 1:].find('+')
        next_operation_mult = expression[plus_index + 1:].find('*')
        # Make sure that if next is not found (-1) we return the last index of string.
        next_operation_plus = len(expression) if next_operation_plus < 0 else next_operation_plus + plus_index + 1
        next_operation_mult = len(expression) if next_operation_mult < 0 else next_operation_mult + plus_index + 1

        right_index = next_operation_plus if next_operation_plus < next_operation_mult else next_operation_mult

        parts = [expression[:left_index+1],
                 expression[left_index+1:plus_index], expression[plus_index + 1:right_index],
                 expression[right_index:]]
        plus_answer = evaluate_expression(parts[1], debug=debug) + evaluate_expression(parts[2], debug=debug)
        if debug:
            print("Resolving addition first: {}".format([parts[1], parts[2]]))

        new_expression = "".join([parts[0], str(plus_answer), parts[3]])
        return evaluate_expression(new_expression, debug=debug)

    # We need to solve a multiplication operation, resolve both sides and multiply them together.
    else:
        parts = [expression[:mult_index], expression[mult_index + 1:]]
        answer = evaluate_expression(parts[0], debug=debug) * evaluate_expression(parts[1], debug=debug)
        if debug:
            print("[*] {} = {}".format(expression, answer))
        return answer

    raise ValueError("Expression could not be parsed: {}".format(expression))


answers = []
for line in lines:
    a = evaluate_expression(line)
    answers.append(a)

print("The sum of all expressions is {}".format(sum(answers)))
