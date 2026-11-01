
from graph import build_graph

import asyncio
from state import AgentState


async def main():
    graph = build_graph()

    initial_state: AgentState = {
        "user_question": "What were the major advances in quantum computing in 2024?",
        "research_results": {},
        "analysis": None,
        "validation_result": None,
        "final_answer": None,
        "validation_attempts": 0,
    }

    result = await graph.ainvoke(initial_state)

    print("\nFinal Answer:")
    print(result["final_answer"])

    print("\nFinal Validation Result:")
    print(result["validation_result"])

    print("\nValidation Attempts:")
    print(result["validation_attempts"])

if __name__ == "__main__":
    asyncio.run(main())

