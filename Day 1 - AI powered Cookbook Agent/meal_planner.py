from llm import meal_planner_llm
from prompts import MEAL_PLANNER_SYSTEM_PROMPT
from recipe_loader import load_recipes


def create_meal_plan(requirements):
    recipes = load_recipes()
    recipes = filter_recipes(recipes, requirements)

    if not recipes:
        raise ValueError("No suitable recipes were found for the user's requirements.")

    recipe_text = "\n\n".join(
        f"""
RECIPE: {recipe.name}

Match Score: {score_recipe(recipe, requirements)}

Tags: {", ".join(recipe.tags)}

Ingredients:

{chr(10).join(
    f"- {ingredient.name}: "
    f"{ingredient.quantity} "
    f"{ingredient.unit or ''}"
    for ingredient in recipe.ingredients
)}

Servings: {recipe.servings}

Prep Time: {recipe.prep_time}

Cook Time: {recipe.cook_time}

Instructions:

{chr(10).join(
    f"- {instruction}"
    for instruction in recipe.instructions
)}

Notes:

{chr(10).join(
    f"- {note}"
    for note in recipe.notes
)}
"""
        for recipe in recipes
    )

    user_prompt = f"""
User requirements:

{requirements.model_dump_json(indent=2)}

Available recipes:

{recipe_text}

Create the meal plan based on these requirements.
"""

    messages = [("system", MEAL_PLANNER_SYSTEM_PROMPT), ("human", user_prompt)]

    return meal_planner_llm.invoke(messages)


# from llm import meal_planner_llm
# from prompts import MEAL_PLANNER_SYSTEM_PROMPT
# from recipe_loader import load_recipes


def normalize_ingredient_name(name: str) -> str:
    """
    Normalize an ingredient name for matching.

    This handles simple variations such as:
    - chicken breast -> chicken breasts
    - onion, diced -> onion
    - broccoli, cut into florets -> broccoli
    """

    name = name.lower().strip()

    # Remove preparation descriptions after a comma.
    name = name.split(",", 1)[0].strip()

    # Remove common preparation words when they appear
    # as part of the ingredient name.
    preparation_words = [
        "cooked",
        "raw",
        "fresh",
        "frozen",
    ]

    words = name.split()

    words = [word for word in words if word not in preparation_words]

    name = " ".join(words)

    # Simple plural normalization.
    if name.endswith("ies"):
        name = name[:-3] + "y"

    elif name.endswith("s") and not name.endswith("ss"):
        name = name[:-1]

    return name


def normalize_unit(unit: str | None) -> str | None:
    """
    Normalize measurement units so singular and plural
    forms can be compared.
    """

    if unit is None:
        return None

    unit = unit.lower().strip()

    unit_aliases = {
        "cup": "cup",
        "cups": "cup",
        "pound": "lb",
        "pounds": "lb",
        "lb": "lb",
        "lbs": "lb",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "tbsp": "tbsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "tsp": "tsp",
        "ounce": "oz",
        "ounces": "oz",
        "oz": "oz",
        "piece": "piece",
        "pieces": "piece",
        "head": "head",
        "heads": "head",
        "clove": "clove",
        "cloves": "clove",
        "gram": "g",
        "grams": "g",
        "g": "g",
        "kilogram": "kg",
        "kilograms": "kg",
        "kg": "kg",
    }

    return unit_aliases.get(unit, unit)


from models import Ingredient


def ingredient_matches(user_ingredient, recipe_ingredient):
    """
    Determine whether the user's ingredient can satisfy
    a recipe ingredient.

    Quantity is compared only when the units are compatible.
    """

    user_name = normalize_ingredient_name(user_ingredient.name)

    recipe_name = normalize_ingredient_name(recipe_ingredient.name)

    # Ingredient names must match.
    if user_name != recipe_name:
        return False

    # If the recipe doesn't specify a quantity,
    # matching the ingredient is enough.
    if recipe_ingredient.quantity is None:
        return True

    # If the user didn't provide a quantity,
    # we cannot verify that they have enough.
    if user_ingredient.quantity is None:
        return False

    # Quantities can only be directly compared
    # when their units are the same.
    user_unit = normalize_unit(user_ingredient.unit)

    recipe_unit = normalize_unit(recipe_ingredient.unit)

    if user_unit != recipe_unit:
        return False

    return user_ingredient.quantity >= recipe_ingredient.quantity


def ingredient_match_type(user_ingredient, recipe_ingredient):
    """
    Classify how well a user's ingredient matches
    a recipe ingredient.

    Returns:
    - "exact"       -> same ingredient and compatible units
    - "unit_mismatch" -> same ingredient, different units
    - None          -> different ingredients
    """

    user_name = normalize_ingredient_name(user_ingredient.name)

    recipe_name = normalize_ingredient_name(recipe_ingredient.name)

    if user_name != recipe_name:
        return None

    user_unit = normalize_unit(user_ingredient.unit)
    recipe_unit = normalize_unit(recipe_ingredient.unit)

    if user_unit != recipe_unit:
        return "unit_mismatch"

    return "exact"


def score_recipe(recipe, requirements):
    """
    Score how well a recipe matches the user's available ingredients.

    Higher scores indicate a stronger match.
    """

    score = 0

    for recipe_ingredient in recipe.ingredients:

        for user_ingredient in requirements.ingredients:

            match_type = ingredient_match_type(user_ingredient, recipe_ingredient)

            if match_type == "exact":
                score += 2
                break

            elif match_type == "unit_mismatch":
                score += 1
                break

    return score


def filter_recipes(recipes, requirements):
    eligible_recipes = []

    user_ingredients = {
        normalize_ingredient_name(ingredient.name)
        for ingredient in requirements.ingredients
    }

    for recipe in recipes:

        # -------------------------
        # Dietary restrictions
        # -------------------------
        excluded = False

        recipe_tags = {tag.lower().strip().replace(" ", "-") for tag in recipe.tags}

        print(recipe.name, recipe.tags)

        for restriction in requirements.dietary_restrictions:
            restriction = restriction.lower()

            if restriction == "vegetarian":
                if "vegetarian" not in recipe_tags:
                    excluded = True

            elif restriction == "no dairy":
                if "dairy-free" not in recipe_tags:
                    excluded = True

        if excluded:
            continue

        # -------------------------
        # Available ingredients
        # -------------------------
        matching_ingredients = []

        for recipe_ingredient in recipe.ingredients:

            for user_ingredient in requirements.ingredients:

                match_type = ingredient_match_type(user_ingredient, recipe_ingredient)

                if match_type in {"exact", "unit_mismatch"}:
                    matching_ingredients.append(
                        (recipe_ingredient.name, user_ingredient.name, match_type)
                    )
                    break
        if len(matching_ingredients) < 2:
            continue

        eligible_recipes.append(recipe)

        print(f"{recipe.name} matches: {matching_ingredients}")

    return eligible_recipes


if __name__ == "__main__":

    recipes = load_recipes()

    requirements = type(
        "Requirements",
        (),
        {
            "dietary_restrictions": ["no dairy"],
            "ingredients": [
                Ingredient(name="chicken breasts", quantity=2, unit="pieces"),
                Ingredient(name="rice", quantity=5, unit="cups"),
                Ingredient(name="broccoli", quantity=2, unit="heads"),
                Ingredient(name="onions", quantity=2, unit="pieces"),
            ],
        },
    )()

    eligible_recipes = filter_recipes(recipes, requirements)

    eligible_recipes.sort(
        key=lambda recipe: score_recipe(recipe, requirements), reverse=True
    )

    print("\nEligible recipes:")

    for recipe in eligible_recipes:
        score = score_recipe(recipe, requirements)

        print(f"- {recipe.name} " f"(score: {score})")
