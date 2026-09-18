import os
from datetime import datetime

from dotenv import load_dotenv

from tavily import TavilyClient
from langchain_core.tools import tool

from pydantic import BaseModel

load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class ResearchRequest(BaseModel):
    topic: str
    year: int | None = None
    isLatest: bool = False


@tool
def calculator(a: float, b: float):
    """Multiply  two numbers together."""
    return a * b


@tool
def word_counter(sentence: str):
    """Count the number of words in a string."""
    return len(sentence.split())


@tool
def research_topic(topic: str, year: int | None = None, is_latest: bool = False):
    """Search the web for information about a topic."""

    current_year = datetime.now().year

    if year is not None:
        search_query = f"{topic} {year}"

    elif is_latest:
        search_query = f"{topic} {current_year}"

    else:
        search_query = topic

    response = tavily_client.search(query=search_query, max_results=3)

    results = []

    for result in response["results"]:
        results.append(
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
            }
        )

    return results
