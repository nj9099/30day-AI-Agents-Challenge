from state import State


def check_research_query(state: State):
    query = state["research_query"]
    history = state.get("research_query_history", [])

    if query in history:
        return {
            "research_query_repeated": True
        }

    return {
        "research_query_repeated": False
    }