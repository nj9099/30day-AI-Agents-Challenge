from typing import TypedDict

class AgentState(TypedDict):
    user_question: str
    research_results: dict
    analysis: dict | None
    validation_result: dict | None
    final_answer: dict | None
    validation_attempts: int

initial_state: AgentState = {
    "user_question": "What were the major advances in quantum computing in 2024?",
    "research_results": {},
    "analysis": None,
    "validation_result": None,
    "final_answer": None,
    "validation_attempts": 0,
}

print(initial_state)