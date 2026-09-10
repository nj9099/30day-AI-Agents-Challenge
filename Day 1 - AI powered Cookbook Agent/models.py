from pydantic import BaseModel, Field

class Ingredient(BaseModel):

    name: str = Field(
        description="Name of the ingredient"
    )

    quantity: float | None = Field(
        description="Amount of the ingredient",
        default=None
    )

    unit: str | None = Field(
        description="Unit of measurement such as pounds, cups, or pieces",
        default=None
    )

class MealRequirements(BaseModel):
    ingredients: list[Ingredient] = Field(
    description="Ingredients the user currently has, including quantities when provided"
)

    dietary_restrictions: list[str] = Field(description="Dietary restrictions or foods the user must avoid")

    servings: int | None = Field(description="Number of people the meal plan should serve", default=None)

    number_of_days: int | None = Field(description="Number of days the meal plan should cover", default=None)

    meal_preferences: list[str] = Field(description="Preferences such as high protein, low calorie, quick meals, etc", default_factory=list)


class IntakeResult(BaseModel):
    complete: bool = Field(description ="Whether enough information has been collected to create a meal plan")

    missing_information: list[str] = Field(description="Information that is still needed from the user", default_factory=list)

    question: str | None = Field(description="The question that was asked to the user", default=None)
    
    requirements: MealRequirements | None = Field(description="Complete meal planning requirements when all necessary information has been collected", default=None)


class PlannedMeal(BaseModel):
    day: int = Field(description="Day number in the meal plan, starting at 1")
    meal_name: str = Field(description="Name of the meal or recipe")
    recipe_source: str | None = Field(description="Recipe file or title used from the knowledge base", default=None)
    ingredients_used: list[str] = Field(description="Ingredients used for this meal", default_factory=list)
    instructions: list[str] = Field(description="Cooking steps for this meal", default_factory=list)
    servings: int | None = Field(description="Number of servings this meal provides", default=None)


# class MealPlan(BaseModel):
#     summary: str = Field(description="Short overview of the meal plan")
#     meals: list[PlannedMeal] = Field(description="Meals organized across the requested number of days")
#     grocery_list: list[str] = Field(
#         description="Ingredients to buy that are not already available",
#         default_factory=list,
#     )
#     notes: list[str] = Field(description="Extra tips for prep, storage, or substitutions", default_factory=list)

class Meal(BaseModel):
    day: int = Field(
        description="Day number in the meal plan"
    )

    recipe_name: str = Field(
        description="Name of the selected recipe"
    )

    servings: int = Field(
        description="Number of servings for this meal"
    )

    reason: str = Field(
        description="Why this recipe was selected"
    )


class MealPlan(BaseModel):
    meals: list[Meal] = Field(
        description="Meals included in the meal plan"
    )

    summary: str = Field(
        description="Short summary of the meal plan"
    )

class Recipe(BaseModel):
    name: str = Field(
        description="Name of the recipe"
    )

    tags: list[str] = Field(
        description="Characteristics or dietary tags for the recipe",
        default_factory=list
    )

    ingredients: list[Ingredient] = Field(
        description="Ingredients required for the recipe",
        default_factory=list
    )

    servings: int | None = Field(
        description="Number of servings the recipe provides",
        default=None
    )

    prep_time: str | None = Field(
        description="Recipe preparation time",
        default=None
    )

    cook_time: str | None = Field(
        description="Recipe cooking time",
        default=None
    )

    instructions: list[str] = Field(
        description="Cooking instructions",
        default_factory=list
    )

    notes: list[str] = Field(
        description="Recipe notes, variations, substitutions, or serving suggestions",
        default_factory=list
    )
