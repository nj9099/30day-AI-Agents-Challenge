import asyncio
from collections import defaultdict

from tools.research_tools import research_topic

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class ResearchPlan(BaseModel):
    topics: list[str] = Field(
        min_length=1,
        max_length=5
    )
    year: int | None = None
    is_latest: bool = False

llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0
    )


planner_llm = llm.with_structured_output(ResearchPlan)

planner_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a research planning assistant.

        Given the user's question:
        1. Generate 1 to 5 focused research topics.
        2. Set `year` to the explicitly requested year, if any.
           If no specific year is requested, set it to null.
        3. Set `is_latest` to true only when the user asks for
           the latest, current, or most recent developments.
           Otherwise, set it to false.
        4. Do not invent a year or assume the user wants the latest
           information unless the question indicates it.
        """
    ),
    ("human", "{user_question}")
])

planner = planner_prompt | planner_llm


# async def researcher(user_question: str) -> dict[str, str]:
#     # return research_topic(user_question)

#     results = {}

#     plan = planer.invoke(user_question)

#     tasks = [
#         research_topic.ainvoke({
#             "query": user_question,
#             "topic": topic
#         })
#         for topic in plan.topics
#     ]

#     research_results = await asyncio.gather(*tasks)

#     # for topic in plan.topics:
#     #     results[topic] = research_topic.invoke({
#     #         "topic": topic,
#     #         "query" : "What were the major advancements in quantum computing in 2024?"
#     #         })

#     return dict(zip(plan.topics, research_results))



async def researcher(user_question: str) -> dict:
    attempt_counts = defaultdict(int)

    plan = planner.invoke(user_question)

    semaphore = asyncio.Semaphore(3)

    tasks = [
        safe_research(user_question, topic, semaphore, plan.year, plan.is_latest, attempt_counts)
        for topic in plan.topics
    ]

    research_results = await asyncio.gather(*tasks)

    research_results_by_topic = {
            result["topic"]: result 
            for result in research_results
        }

    failed_topics = [
        item["topic"]
        for item in research_results
        if not item["success"]
    ]

    print(f"Failed topics: {failed_topics}")

    if failed_topics:
        print(f"Retrying failed topics: {failed_topics}")

        retry_tasks = [
            safe_research(user_question, topic, semaphore, plan.year, plan.is_latest, attempt_counts)
            for topic in failed_topics
        ]

        retry_results = await asyncio.gather(*retry_tasks)

        for item in retry_results:
            research_results_by_topic[item["topic"]] = item

            print(
                f"Retry {'succeeded' if item['success'] else 'failed'}: "
                f"{item['topic']}"
            )

    return research_results_by_topic


async def safe_research( 
    user_question: str, 
    topic: str,
    semaphore: asyncio.Semaphore,
    year: int | None,
    is_latest: bool,
    attempt_counts: dict
    ):
    try:
        attempt_counts[topic] += 1

        if "quantum error correction" in topic.lower() and attempt_counts[topic] == 1:
            raise TimeoutError("Simulated first attempt failure")
            
        async with semaphore:
            result = await research_topic.ainvoke({
                "query": user_question,
                "topic": topic,
                "year": year,
                "is_latest":is_latest
            })
            print(f"\nResearch evidence for: {topic}")
            print(result)

        return {
                "topic": topic,
                "success": True,
                "result": result,
                "error": None
            }

    except Exception as error:
        return {
                "topic": topic,
                "success": False,
                "result": None,
                "error": str(error)
            }
