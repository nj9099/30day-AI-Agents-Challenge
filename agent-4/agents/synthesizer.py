
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


class ResearchAnswer(BaseModel):
    answer: str = Field(
        description="The final answer to the user's original question"
    )
    key_takeaways: list[str] = Field(
        description="The most important conclusions supported by the evidence"
    )
    limitations: list[str] = Field(
        description="Important evidence gaps, uncertainties, and limitations"
    )


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

synthesizer_llm = llm.with_structured_output(ResearchAnswer)


synthesizer_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a research report synthesizer.

    Your task is to produce a clear, useful final answer to the
    user's original question using the supplied research analysis
    and validation results.

    Follow these rules:

    1. Answer the original question directly.
       Organize the response logically and prioritize the most
       important findings.

    2. Use only claims supported by the supplied analysis and
       research evidence. Never invent facts, statistics, sources,
       quotations, or research findings.

    3. Preserve uncertainty.
       Distinguish established findings from interpretations,
       tentative conclusions, and unresolved questions.
       Never present uncertain claims as established facts.

    4. Handle missing information honestly.
       If research failed or evidence is insufficient, explain
       the relevant limitation. Never interpret a failed research
       call as proof that a claim is false or that no progress
       occurred.

    5. Respect the validation result.
       If the analysis is invalid, do not present it as a
       reliable, definitive answer. Explain that the available
       evidence is insufficient or that significant issues remain.
       Do not silently ignore the validator's reason or missing
       information.

    6. Be useful and concise.
       Avoid repetition, irrelevant background, and unnecessary
       technical jargon. Use clear language appropriate to the
       user's question.

    7. Construct the output fields consistently.
       - answer: A coherent response to the original question.
       - key_takeaways: The most important supported conclusions.
       - limitations: Important evidence gaps and uncertainties.

    8. Keep the answer proportionate to the evidence.
       Do not make the answer sound more comprehensive or
       certain than the available research justifies.

    Your goal is not to make incomplete research look complete.
    Your goal is to communicate what the evidence establishes,
    what it suggests, and what remains unknown.
    """),
    ("human", """
    User question:
    {user_question}

    Research results:
    {research_results}

    Analyst's analysis:
    {analysis}

    Validation result:
    {validation_result}
    """)
])

synthesizer_chain = synthesizer_prompt | synthesizer_llm

async def synthesize(
    user_question: str,
    research_results: dict,
    analysis: dict,
    validation_result: dict
) -> ResearchAnswer:
    
    result = await synthesizer_chain.ainvoke({
        "user_question": user_question,
        "research_results": research_results,
        "analysis": analysis,
        "validation_result": validation_result
    })

    return result