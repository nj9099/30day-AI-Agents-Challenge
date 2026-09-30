from typing import Annotated, TypedDict

from langgraph.graph import add_messages

# 1. Define the graph's state
class State(TypedDict):

    messages: Annotated[list, add_messages]

    research_needed: str
    research_year: int | None
    research_subject: str
    research_is_latest: bool
    research_results: list
    research_query: str
    research_query_history: list[str]
    research_query_repeated: bool

    research_valid: bool
    research_validation_reason: str
    research_missing_information: str

    research_attempts: int
