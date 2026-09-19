from email import message
from re import S
from typing import Annotated, Literal, TypedDict
from pydantic import BaseModel, Field, model_validator

from dotenv import load_dotenv
from urllib3 import response
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, tool_node

from tools import calculator, word_counter, research_topic

load_dotenv()


# 1. Define the graph's state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    research_needed: str
    research_year: int | None
    research_subject: str
    research_is_latest: bool
    research_results: list
    research_valid: str
    research_validation_reason: str
    research_attempts: int


class Classification(BaseModel):
    complexity: Literal["simple", "complex"] = Field(
        description="Whether the question is simple or complex"
    )


class ToolClassification(BaseModel):
    isToolNeeded: Literal["yes", "no"] = Field(
        description="Whether the question is an arithemetic problem"
    )


class ResearchIntent(BaseModel):
    topic: str = Field(description="The main research topic without the time period")

    year: int | None = Field(
        default=None,
        description="The specific year requested by the user. "
        "Use None if no specific year was requested.",
    )

    is_latest: bool = Field(
        description="True only when the user explicitly asks for the latest, "
        "current, recent, or up-to-date information. "
        "If a specific year is requested, this must be False."
    )

    @model_validator(mode="after")
    def validate_time_period(self):
        if self.year is not None:
            self.is_latest = False

        return self


class ResearchClassification(BaseModel):
    isResearch: Literal["yes", "no"] = Field(
        description="Whether the user's question requires web research"
    )


class ResearchValidation(BaseModel):
    is_valid: Literal["yes", "no"] = Field(
        description=(
            "Whether the research results are relevant to the user's "
            "question and requested time period."
        )
    )

    reason: str = Field(description="Brief explanation for the validation decision.")


# Create LLM node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

classifier_llm = llm.with_structured_output(Classification)
tool_classifier_llm = llm.with_structured_output(ToolClassification)
research_classifier = llm.with_structured_output(ResearchIntent)
research_decision_llm = llm.with_structured_output(ResearchClassification)
research_validator = llm.with_structured_output(ResearchValidation)

llm_with_tools = llm.bind_tools([calculator, word_counter, research_topic])
tool_node = ToolNode([calculator, word_counter, research_topic])


def agent(state: State):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def route_tools(state: State):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


def route_research(state: State):
    if state["research_needed"] == "yes":
        return "research"
    return "retry"


def route_validation(state: State):
    if state["research_valid"] == "yes":
        return "synthesis"

    if state["research_attempts"] < 2:
        return "retry"

    return "synthesis"


def research(state: State):
    attempt = state["research_attempts"] + 1

    question = state["messages"][0].content

    intent = research_classifier.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Extract the user's research intent. "
                    "Identify the main research topic, any explicitly "
                    "requested year, and whether the user wants the "
                    "latest information."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )

    results = research_topic.invoke(
        {
            "year": intent.year,
            "topic": intent.topic,
            "is_latest": intent.is_latest,
        }
    )

    return {
        "research_subject": intent.topic,
        "research_year": intent.year,
        "research_is_latest": intent.is_latest,
        "research_results": results,
        "research_attempts": attempt,
    }


def research_decision(state: State):
    question = state["messages"][0].content

    response = research_decision_llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Determine whether the user's question requires "
                    "web research. Return 'yes' if the question asks "
                    "for factual information that should be researched "
                    "from the web, especially current, recent, or "
                    "specific factual information. Otherwise return 'no'."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]
    )

    return {"research_needed": response.isResearch}


def research_sysnthesis(state: State):
    question = state["messages"][0].content
    results = state["research_results"]

    research_text = "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result['content']}"
        for result in results
    )

    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using the research results "
                    "provided below. Synthesize the information clearly. "
                    "Do not invent facts that are not supported by the "
                    "research. If the sources disagree or the evidence is "
                    "limited, mention that."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n" f"Research results:\n{research_text}"
                ),
            },
        ]
    )

    return {"messages": [response]}


def validate_research(state: State):
    question = state["messages"][0].content
    results = state["research_results"]

    research_text = "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result['content']}"
        for result in results
    )

    response = research_validator.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Evaluate whether the research results are relevant "
                    "to the user's question. Pay particular attention to "
                    "the requested year or time period. "
                    "Return 'yes' only if the results are sufficiently "
                    "relevant to answer the question. "
                    "Return 'no' if the results contain a significant "
                    "topic or time-period mismatch."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n" f"Research results:\n{research_text}"
                ),
            },
        ]
    )

    return {
        "research_valid": response.is_valid,
        "research_validation_reason": response.reason,
    }


# 3. Create the graph
graph = StateGraph(State)

graph.add_node("agent", agent)
graph.add_node("tools", tool_node)
graph.add_node("research", research)
graph.add_node("research_decision", research_decision)
graph.add_node("research_synthesis", research_sysnthesis)
graph.add_node("validate_research", validate_research)

graph.add_edge(START, "research_decision")

graph.add_conditional_edges(
    "research_decision",
    route_research,
    {
        "research": "research",
        "agent": "agent",
    },
)

graph.add_conditional_edges("agent", route_tools, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

graph.add_edge("research", "validate_research")

graph.add_conditional_edges(
    "validate_research",
    route_validation,
    {"synthesis": "research_synthesis", "retry": "research"},
)
graph.add_edge("research_synthesis", END)


# 6. Compile the graph
app = graph.compile()

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Who was the best scorer in the 2023 NBA season?",
            }
        ],
        "research_attempts": 0,
    }
)

print(result["research_attempts"])
print(result["research_valid"])
print(result["messages"][-1].content)
