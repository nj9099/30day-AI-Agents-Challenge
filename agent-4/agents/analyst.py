from pydantic import Field, BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()


class Analysis(BaseModel):
    key_findings: list[str] = Field(
        description="Main findings supported by the research"
    )
    evidence: list[str] = Field(
        description="Supporting evidence from the supplied results"
    )
    gaps: list[str] = Field(description="Missing information and unresolved questions")
    analysis: str = Field(description="Overall interpretation of the findings")


llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

analyst_llm = llm.with_structured_output(Analysis)

analyst_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        You are a research analyst.

        Your task is to analyze research results and produce
        evidence-grounded conclusions that answer the user's question.

        Follow these rules:
        1. Identify the most important findings across the research.
        2. Support conclusions using the supplied research evidence.
        3. Identify missing information and unresolved questions.
        4. Never invent facts, sources, or evidence.
        5. When a topic's research failed, identify it as an unresolved
        information gap. Do not include it among substantive findings
        unless other successful research results independently support
        those findings.
        6. Distinguish established findings from uncertainty.
        7. Base your overall analysis on the available evidence.
        8. A research-tool failure describes a limitation of information
        retrieval, not a finding about the subject being researched.
        Never infer that a field lacks progress, results, or evidence
        merely because a research call failed.
        Evaluate the quality of the supplied evidence before presenting
        a claim as a finding. Placeholder text, vague summaries, and
        statements without supporting details must not be presented as
        verified facts. Explicitly communicate when evidence is
        insufficient to establish a claim.
        """,
        ),
        (
            "human",
            """
        User question:
        {user_question}

        Research results:
        {research_results}
        """,
        ),
    ]
)

analyst_chain = analyst_prompt | analyst_llm

async def analyze(
    user_question: str,
    research_results: dict
) -> Analysis:

    results = await analyst_chain.ainvoke({
        "user_question": user_question,
        "research_results": research_results

    })

    return results
