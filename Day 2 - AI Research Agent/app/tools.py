
from langchain_core.tools import tool

@tool
def calculator(a: float, b: float):
    """Multiply  two numbers together."""
    return a*b