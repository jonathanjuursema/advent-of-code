f = open("input.txt", "r")
raw_input_foods = f.read().splitlines()

allergen_dict = {}

for raw_food in raw_input_foods:
    split = raw_food.split(" (contains ")
    this_product_ingredients = split[0].split(" ")
    allergens = split[1][:-1].split(", ")

    for allergen in allergens:
        if allergen in allergen_dict.keys():
            new_allergen_ingredients = []
            for ingredient in allergen_dict[allergen].copy():
                if ingredient in this_product_ingredients:
                    new_allergen_ingredients.append(ingredient)
            allergen_dict[allergen] = new_allergen_ingredients
        else:
            allergen_dict[allergen] = this_product_ingredients

single_allergen_dict = {}

while len(single_allergen_dict.keys()) != len(allergen_dict.keys()):
    for allergen in allergen_dict.keys():
        if len(allergen_dict[allergen]) == 1:
            single_allergen_dict[allergen] = allergen_dict[allergen][0]
        else:
            new_ingredients = allergen_dict[allergen].copy()
            for solved_allergen, solved_ingredient in single_allergen_dict.items():
                if solved_ingredient in new_ingredients:
                    new_ingredients.remove(solved_ingredient)
            allergen_dict[allergen] = new_ingredients

answer_list = []
for allergen in sorted(single_allergen_dict.keys()):
    answer_list.append(single_allergen_dict[allergen])

print("Puzzle answer:\n{}".format(",".join(answer_list)))
