from state import State

from config.llm import research_decision_llm

def research_decision(state: State):
    question = state["messages"][0].content

    response = research_decision_llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Determine whether the user's question requires "
                    "web research. Return 'yes' if the question asks "
                    "for factual information that should be researched "
                    "from the web, especially current, recent, or "
                    "specific factual information. Otherwise return 'no'."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )

    return {"research_needed": response.isResearch}