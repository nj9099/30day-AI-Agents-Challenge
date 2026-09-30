from state import State

from config.llm import llm

def research_synthesis(state: State):
    question = state["messages"][0].content
    results = state["research_results"]

    research_valid = state["research_valid"]
    validation_reason = state["research_validation_reason"]
    missing_information = state["research_missing_information"]

    research_text = "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result['content']}"
        for result in results
    )

    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using the research results "
                    "provided below. Synthesize the information clearly. "
                    "Do not invent facts that are not supported by the "
                    "research. If the sources disagree or the evidence is "
                    "limited, mention that."
                    "If the research was not validated as sufficient, do not present"
                    "the answer as fully established. Clearly state what the research"
                    "supports and what information remains missing."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n" f"Research results:\n{research_text}\n\n"
                    f"Research valid:\n{research_valid}\n\n"
                    f"Reason:\n{validation_reason}\n\n"
                    f"Missing information:\n{missing_information}"
                ),
            },
        ]
    )

    return {"messages": [response]}