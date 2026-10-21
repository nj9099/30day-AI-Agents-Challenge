
import asyncio
from synthesizer import synthesize


async def main():
    user_question = (
        "What were the major advances in quantum computing in 2024?"
    )

    research_results = {
        "Quantum hardware": {
            "topic": "Quantum hardware",
            "success": True,
            "result": "Mock evidence about hardware improvements.",
            "error": None,
        },
        "Quantum error correction": {
            "topic": "Quantum error correction",
            "success": False,
            "result": None,
            "error": "Simulated timeout after retry",
        },
    }

    analysis = """
    The supplied research result contains a vague statement about
    quantum hardware improvements, but it does not provide enough
    detail to establish what improved or how significant the advances
    were. The research call for quantum error correction failed, so
    no conclusion can be drawn about advances in that area.
    """

    validation_result = {
        "is_valid": False,
        "reason": (
            "The analysis lacks sufficient evidence to answer "
            "the original question reliably."
        ),
        "missing_information": [
            "Specific evidence about quantum hardware improvements.",
            "Reliable research about quantum error correction.",
        ],
    }

    result = await synthesize(
        user_question=user_question,
        research_results=research_results,
        analysis=analysis,
        validation_result=validation_result,
    )

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
