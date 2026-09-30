from state import State

from config.llm import research_classifier
from tools.research_tools import research_topic



def research(state: State):
    attempt = state["research_attempts"] + 1
    query_history = state.get("research_query_history", [])

    question = state["messages"][0].content

    intent = research_classifier.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Extract the user's research intent. "
                    "Identify the main research topic, any explicitly "
                    "requested year, and whether the user wants the "
                    "latest information."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )


    query = state.get('research_query')

    if not query:
        query = intent.topic
        
        if intent.year is not None:
            query += f" {intent.year}"
        elif intent.is_latest:
            query += " latest"
    
    query_history = query_history + [query]

    print("Research query : ", query)

    results = research_topic.invoke(
        {
            "query": query,
            "year": intent.year,
            "topic": intent.topic,
            "is_latest": intent.is_latest,
        }
        )

    return {
        "research_subject": intent.topic,
        "research_year": intent.year,
        "research_is_latest": intent.is_latest,
        "research_query": query,
        "research_query_history": query_history,
        "research_results": results,
        "research_attempts": attempt,
    }



