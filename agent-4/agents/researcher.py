import asyncio
from tools.research_tools import research_topic

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from collections import defaultdict


class ResearchPlan(BaseModel):
    topics: list[str] = Field(
        min_length=1,
        max_length=5
    )

llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0
    )


planer = llm.with_structured_output(ResearchPlan)

attempt_counts = defaultdict(int)


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
    plan = planer.invoke(user_question)

    semaphore = asyncio.Semaphore(3)

    tasks = [
        safe_research(user_question, topic, semaphore)
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
            safe_research(user_question, topic, semaphore)
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
    semaphore: asyncio.Semaphore
    ):
    try:
        attempt_counts[topic] += 1
        if topic == 'Advancements in quantum error correction techniques' and attempt_counts[topic] == 1:
            raise TimeoutError("Simulated first attempt failure")
        async with semaphore:
            result = await research_topic.ainvoke({
                "query": user_question,
                "topic": topic
            })

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
