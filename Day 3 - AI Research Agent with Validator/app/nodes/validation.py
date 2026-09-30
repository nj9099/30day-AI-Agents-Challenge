from state import State

from config.llm import llm, research_validator

def validate_research(state: State):
    question = state["messages"][0].content
    results = state["research_results"]

    research_text = "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result['content']}"
        for result in results
    )

    response = research_validator.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Evaluate whether the research results are relevant "
                    "to the user's question. For this test, consider the "
                    "research invalid unless the results contain specific "
                    "information about quantum hardware manufacturing "
                    "techniques used in 2023. Return valid=True only when "
                    "that specific information is present. Otherwise, "
                    "return valid=False and clearly describe the missing "
                    "information."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n" f"Research results:\n{research_text}"
                ),
            },
        ]
    )

    return {
        "research_valid": response.valid,
        "research_validation_reason": response.reason,
        "research_missing_information": response.missing_information,
    }
