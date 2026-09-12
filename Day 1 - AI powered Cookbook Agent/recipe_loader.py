from pathlib import Path
import re

from models import Recipe, Ingredient


RECIPES_DIR = Path(__file__).resolve().parent / "recipes"


# Common recipe units and their normalized forms
UNIT_ALIASES = {
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
    "gram": "g",
    "grams": "g",
    "g": "g",
    "kilogram": "kg",
    "kilograms": "kg",
    "kg": "kg",
    "clove": "clove",
    "cloves": "clove",
    "head": "head",
    "heads": "head",
    "piece": "piece",
    "pieces": "piece",
}


# Longer units should be checked before shorter ones.
UNIT_PATTERN = "|".join(
    sorted([re.escape(unit) for unit in UNIT_ALIASES], key=len, reverse=True)
)


def parse_quantity(value: str) -> float:
    """
    Convert recipe quantities into floats.

    Examples:
        2       -> 2.0
        1/2     -> 0.5
        1 1/2   -> 1.5
        2.5     -> 2.5
    """

    value = value.strip()

    # Mixed number: 1 1/2
    mixed_match = re.fullmatch(r"(\d+)\s+(\d+)/(\d+)", value)

    if mixed_match:
        whole = int(mixed_match.group(1))
        numerator = int(mixed_match.group(2))
        denominator = int(mixed_match.group(3))

        return whole + numerator / denominator

    # Simple fraction: 1/2
    fraction_match = re.fullmatch(r"(\d+)/(\d+)", value)

    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))

        return numerator / denominator

    # Integer or decimal
    return float(value)


def parse_ingredient(item: str) -> Ingredient:
    """
    Convert one ingredient line into an Ingredient object.
    """

    item = item.lstrip("- ").strip()

    # Match the quantity at the beginning.
    quantity_pattern = r"(?P<quantity>\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)"

    pattern = re.compile(
        rf"^{quantity_pattern}\s*"
        rf"(?P<unit>{UNIT_PATTERN})?"
        rf"(?:\s+)?"
        rf"(?P<name>.+)$",
        re.IGNORECASE,
    )

    match = pattern.match(item)

    if not match:
        return Ingredient(name=item)

    quantity = parse_quantity(match.group("quantity"))

    unit = match.group("unit")

    if unit:
        unit = UNIT_ALIASES[unit.lower()]

    name = match.group("name").strip()

    return Ingredient(name=name, quantity=quantity, unit=unit)


def load_recipes() -> list[Recipe]:
    recipes = []

    for recipe_file in RECIPES_DIR.glob("*.md"):

        content = recipe_file.read_text(encoding="utf-8")

        sections = {}
        current_section = None
        name = recipe_file.stem

        # --------------------------------------------------
        # Parse Markdown sections
        # --------------------------------------------------

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("# ") and not line.startswith("## "):

                name = line[2:].strip()

            elif line.startswith("## "):

                current_section = line[3:].strip().lower()
                sections[current_section] = []

            elif line and current_section:

                sections[current_section].append(line)

        # --------------------------------------------------
        # Tags
        # --------------------------------------------------

        tags = []

        if sections.get("tags"):

            tags = [
                tag.strip() for tag in sections["tags"][0].split(",") if tag.strip()
            ]

        # Some recipes use "Dietary Information"
        elif sections.get("dietary information"):

            tags = [
                item.lstrip("- ").strip()
                for item in sections["dietary information"]
                if item.strip()
            ]

        # --------------------------------------------------
        # Ingredients
        # --------------------------------------------------

        ingredients = [
            parse_ingredient(item)
            for item in sections.get("ingredients", [])
            if item.strip()
        ]

        # --------------------------------------------------
        # Instructions
        # --------------------------------------------------

        instructions = []

        for item in sections.get("instructions", []):

            item = item.strip()

            # Remove numbered-list prefixes:
            # 1. Cut chicken...
            numbered_match = re.match(r"^\d+\.\s*(.+)$", item)

            if numbered_match:
                item = numbered_match.group(1)

            instructions.append(item)

        # --------------------------------------------------
        # Notes
        # --------------------------------------------------

        notes = [
            item.lstrip("- ").strip()
            for item in sections.get("notes", [])
            if item.strip()
        ]

        # --------------------------------------------------
        # Servings
        # --------------------------------------------------

        servings = None

        if sections.get("servings"):

            try:
                servings = int(sections["servings"][0])
            except ValueError:
                pass

        # --------------------------------------------------
        # Preparation Time
        # Supports both:
        #   ## Prep Time
        #   ## Preparation Time
        # --------------------------------------------------

        prep_time = None

        if sections.get("prep time"):
            prep_time = sections["prep time"][0]

        elif sections.get("preparation time"):
            prep_time = sections["preparation time"][0]

        # --------------------------------------------------
        # Cooking Time
        # Supports both:
        #   ## Cook Time
        #   ## Cooking Time
        # --------------------------------------------------

        cook_time = None

        if sections.get("cook time"):
            cook_time = sections["cook time"][0]

        elif sections.get("cooking time"):
            cook_time = sections["cooking time"][0]

        # --------------------------------------------------
        # Create Recipe object
        # --------------------------------------------------

        recipe = Recipe(
            name=name,
            tags=tags,
            ingredients=ingredients,
            servings=servings,
            prep_time=prep_time,
            cook_time=cook_time,
            instructions=instructions,
            notes=notes,
        )

        recipes.append(recipe)

    return recipes


# ------------------------------------------------------
# Temporary parser test
# ------------------------------------------------------

if __name__ == "__main__":

    recipes = load_recipes()

    for recipe in recipes:

        print(f"\n{recipe.name}")

        for ingredient in recipe.ingredients:

            print(
                f"  {ingredient.name} | "
                f"{ingredient.quantity} | "
                f"{ingredient.unit}"
            )
