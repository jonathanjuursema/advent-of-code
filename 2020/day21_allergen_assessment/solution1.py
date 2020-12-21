f = open("input.txt", "r")
raw_input_foods = f.read().splitlines()

products = []
allergen_to_ingredient = {}

for raw_food in raw_input_foods:
    split = raw_food.split(" (contains ")
    this_product_ingredients = split[0].split(" ")
    allergens = split[1][:-1].split(", ")

    products.append({
        'ingredients': this_product_ingredients,
        'allergens': allergens
    })

    for allergen in allergens:
        if allergen in allergen_to_ingredient.keys():
            new_allergen_ingredients = []
            for ingredient in allergen_to_ingredient[allergen].copy():
                if ingredient in this_product_ingredients:
                    new_allergen_ingredients.append(ingredient)
            allergen_to_ingredient[allergen] = new_allergen_ingredients
        else:
            allergen_to_ingredient[allergen] = this_product_ingredients


def is_safe(ingredient, allergen_dict):
    for allergen in allergen_dict.keys():
        if ingredient in allergen_dict[allergen]:
            return False
    return True


safe_ingredient_count = 0
for product in products:
    for ingredient in product['ingredients']:
        if is_safe(ingredient=ingredient, allergen_dict=allergen_to_ingredient):
            safe_ingredient_count += 1

print("{} ingredients are safe.".format(safe_ingredient_count))