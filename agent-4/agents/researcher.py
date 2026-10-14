from tools.research_tools import research_topic

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI


class ResearchPlan(BaseModel):
    topics: list[str] = Field(
        min_length=1,
        max_length=5
    )


def researcher(user_question: str) -> dict[str, str]:
    # return research_topic(user_question)

    results = {}

    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0
    )


    planer = llm.with_structured_output(ResearchPlan)

    plan = planer.invoke("What were the major advancements in quantum computing in 2024?")

    for topic in plan.topics:
        results[topic] = research_topic.invoke({
            "topic": topic,
            "query" : "What were the major advancements in quantum computing in 2024?"
            })

    return results


