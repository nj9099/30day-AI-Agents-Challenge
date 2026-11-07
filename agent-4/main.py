import asyncio

from graph import build_graph
from state import initial_state

async def main():
    user_question = "What were the major advances in quantum computing in 2024?"

    app = build_graph()

    state = {
        **initial_state,
        "user_question": user_question
    }
    
    result = await app.ainvoke(state)

    print("\nFinal Answer: ")
    print(result["final_answer"])

if __name__ == "__main__":
    asyncio.run(main())