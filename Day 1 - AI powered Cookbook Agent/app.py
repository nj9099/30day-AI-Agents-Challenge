from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path

# Core agent imports (relative to project root when the file is placed there)
from meal_planner import create_meal_plan
from models import MealRequirements, Ingredient, MealPlan
from recipe_loader import load_recipes

app = FastAPI()

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---------- Helper utilities ----------
def _load_all_recipes():
    return load_recipes()

def _unique_ingredients(recipes: List):
    ingredients = set()
    for r in recipes:
        for ing in r.ingredients:
            ingredients.add(ing.name.lower())
    return sorted(ingredients)

def _unique_tags(recipes: List):
    tags = set()
    for r in recipes:
        for t in r.tags:
            tags.add(t.lower())
    return sorted(tags)

COMMON_RESTRICTIONS = ["vegetarian", "no dairy", "gluten free", "nut free", "vegan"]
COMMON_PREFERENCES = ["high protein", "quick meals", "low calorie", "meat based", "batch cooking"]

class OptionsResponse(BaseModel):
    ingredients: List[str]
    dietary_restrictions: List[str]
    meal_preferences: List[str]
    tags: List[str]

class MealPlanRequest(BaseModel):
    ingredients: List[Ingredient] = Field(description="User available ingredients")
    dietary_restrictions: List[str] = Field(default_factory=list)
    servings: Optional[int] = Field(default=None)
    number_of_days: Optional[int] = Field(default=None)
    meal_preferences: List[str] = Field(default_factory=list)

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/options", response_model=OptionsResponse)
async def get_options():
    recipes = _load_all_recipes()
    return OptionsResponse(
        ingredients=_unique_ingredients(recipes),
        dietary_restrictions=COMMON_RESTRICTIONS,
        meal_preferences=COMMON_PREFERENCES,
        tags=_unique_tags(recipes),
    )

@app.get("/api/recipes")
async def get_recipes():
    recipes = _load_all_recipes()
    return JSONResponse(content=[r.dict() for r in recipes])

@app.post("/api/plan", response_model=MealPlan)
async def plan_meal(request: MealPlanRequest):
    requirements = MealRequirements(
        ingredients=request.ingredients,
        dietary_restrictions=request.dietary_restrictions,
        servings=request.servings,
        number_of_days=request.number_of_days,
        meal_preferences=request.meal_preferences,
    )
    try:
        plan = create_meal_plan(requirements)
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
