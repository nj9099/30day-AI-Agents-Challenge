import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from models import IntakeResult, MealPlan

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

intake_llm = llm.with_structured_output(IntakeResult)

meal_planner_llm = llm.with_structured_output(MealPlan)