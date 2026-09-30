from state import State
from config.llm import research_refiner


def refine_research_query(state: State):
    response = research_refiner.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Improve the web search query based on the research "
                    "validation feedback. The new query should address "
                    "the missing information while preserving the original "
                    "topic and requested time period. Return only a concise "
                    "search query."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original query: {state['research_query']}\n"
                    f"Research subject: {state['research_subject']}\n"
                    f"Research year: {state['research_year']}\n"
                    f"Validation reason: "
                    f"{state['research_validation_reason']}\n"
                    f"Missing information: "
                    f"{state['research_missing_information']}"
                ),
            },
        ]
    )

    return {
        "research_query": response.refined_query
    }