from llm import intake_llm
from prompts import INTAKE_SYSTEM_PROMPT
from meal_planner import create_meal_plan


def main():
    conversation = []

    print("Meal Prep AI")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break

        conversation.append(
            ("human", user_input)
        )

        messages = [
            ("system", INTAKE_SYSTEM_PROMPT),
            *conversation
        ]

        result = intake_llm.invoke(messages)

        if result.complete:
            print("\nIntake complete!")
            print("\nRequirements:")
            print(result.requirements)

            # Create the meal plan
            meal_plan = create_meal_plan(result.requirements)

            print("\nMeal Plan")
            print("=" * 50)
            print(meal_plan.summary)

            for meal in meal_plan.meals:
                print(f"\nDay {meal.day}")
                print(f"Recipe: {meal.recipe_name}")
                print(f"Servings: {meal.servings}")
                print(f"Reason: {meal.reason}")

            break

        print(f"\nAssistant: {result.question}\n")

        conversation.append(
            ("assistant", result.question)
        )


if __name__ == "__main__":
    main()