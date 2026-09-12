from pathlib import Path
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from recipe_loader import load_recipes

from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = str(Path(__file__).resolve().parent / "chroma_db")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def load_recipe_documents():
    recipes = load_recipes()

    documents = []

    for recipe in recipes:
        content = f"""
Recipe: {recipe.name}

Tags: {", ".join(recipe.tags)}

Ingredients:
{chr(10).join(
    f"- {ingredient.name}: {ingredient.quantity} {ingredient.unit or ''}"
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

        documents.append(
            Document(
                page_content=content.strip(), metadata={"recipe_name": recipe.name}
            )
        )

    return documents


def load_vector_store():
    store = Chroma(
        collection_name="recipes",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
    try:
        existing = store.get()
        if not existing or len(existing.get("ids", [])) == 0:
            docs = load_recipe_documents()
            if docs:
                store.add_documents(docs)
    except Exception:
        pass
    return store


def build_retrieval_query(requirements):
    ingredients = ", ".join(ingredient.name for ingredient in requirements.ingredients)

    restrictions = ", ".join(requirements.dietary_restrictions)

    preferences = ", ".join(requirements.meal_preferences)

    return f"""
Ingredients: {ingredients}
Dietary restrictions: {restrictions}
Meal preferences: {preferences}
""".strip()


def retrieve_recipes(requirements, eligible_recipes):
    query = build_retrieval_query(requirements)

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(search_kwargs={"k": 8})

    results = retriever.invoke(query)

    eligible_names = {recipe.name for recipe in eligible_recipes}

    filtered_results = [
        document
        for document in results
        if document.metadata["recipe_name"] in eligible_names
    ]

    return filtered_results


if __name__ == "__main__":
    from models import MealRequirements, Ingredient
    from recipe_loader import load_recipes
    from meal_planner import filter_recipes

    requirements = MealRequirements(
        ingredients=[
            Ingredient(name="chicken breast"),
            Ingredient(name="rice"),
            Ingredient(name="eggs"),
            Ingredient(name="broccoli"),
            Ingredient(name="onions"),
        ],
        dietary_restrictions=["no dairy"],
        servings=2,
        number_of_days=5,
        meal_preferences=["meat based"],
    )

    recipes = load_recipes()

    eligible_recipes = filter_recipes(recipes, requirements)

    results = retrieve_recipes(requirements, eligible_recipes)

    for document in results:
        print("\n---")
        print(document.metadata)
