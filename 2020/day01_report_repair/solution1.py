import itertools
import numpy

f = open("input.txt", "r")
expenses = [int(expense) for expense in f.readlines()]

for combination in itertools.product(expenses, repeat=2):
    if sum(combination) == 2020:
        print("sum({}) = 2020".format(combination))
        print("product({}) = {}".format(combination, numpy.prod(combination)))
