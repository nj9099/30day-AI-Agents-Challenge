import asyncio

from agents.researcher import researcher
from agents.analyst import analyze
from agents.validator import validate

async def main():
    user_question = "What were the major advances in quantum computing in 2024?"

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

    careful_analysis = """
        The supplied research result contains a vague statement about
        quantum hardware improvements, but it does not provide enough
        detail to establish what improved or how significant the advances
        were. The research call for quantum error correction failed,
        so no conclusion can be drawn from the available results about
        advances in that area. Further evidence is needed to answer the
        question reliably.
        """

    result = await validate(
        user_question=user_question,
        research_results=research_results,
        analysis=careful_analysis,
    )

    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())