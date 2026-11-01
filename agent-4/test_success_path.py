import asyncio
from graph import build_graph
from agents.validator import validate
from agents.validator import ValidationResult


validation_calls = 0

async def mock_validate(*args, **kwargs):
    global validation_calls
    validation_calls += 1

    if validation_calls == 1:
        return ValidationResult(
            is_valid=False,
            reason="Missing error correction research.",
            missing_information=["Advances in quantum error correction"]
        )

    return ValidationResult(
        is_valid=True,
        reason="Mock validation successful.",
        missing_information=[]
    )

async def mock_researcher(user_question):
    import graph

    graph.researcher_calls += 1

    if graph.researcher_calls == 1:
        return {
            "hardware": {
                "success": True,
                "evidence": "Initial hardware research"
            }
        }

    return {
        "error_correction": {
            "success": True,
            "evidence": "Follow-up error correction research"
        }
    }

async def main():
    # Temporarily replace the real validator
    import graph

    graph.researcher_calls = 0
    graph.researcher = mock_researcher
    graph.validate = mock_validate

    workflow = build_graph()

    initial_state = {
        "user_question": "What were the major advances in quantum computing in 2024?",
        "research_results": {},
        "analysis": None,
        "validation_result": None,
        "final_answer": None,
        "validation_attempts": 0,
    }

    result = await workflow.ainvoke(initial_state)

    print("\nFinal Answer:")
    print(result["final_answer"])

    print("\nFinal Validation:")
    print(result["validation_result"])

    print("\nValidation Attempts:")
    print(result["validation_attempts"])


if __name__ == "__main__":
    asyncio.run(main())