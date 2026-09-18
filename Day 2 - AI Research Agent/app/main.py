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


# Create LLM node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

classifier_llm = llm.with_structured_output(Classification)
tool_classifier_llm = llm.with_structured_output(ToolClassification)
research_classifier = llm.with_structured_output(ResearchIntent)
research_decision_llm = llm.with_structured_output(ResearchClassification)

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
    return "agent"


def research(state: State):
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
        "research_results": results
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


# 3. Create the graph
graph = StateGraph(State)

graph.add_node("agent", agent)
graph.add_node("tools", tool_node)
graph.add_node("research", research)
graph.add_node("research_decision", research_decision)

graph.add_edge(START, "research_decision")

graph.add_conditional_edges(
    "research_decision",
    route_research,
    {
        "research": "research",
        "agent": "agent",
    },
)

graph.add_edge("research", END)

graph.add_conditional_edges("agent", route_tools, {"tools": "tools", END: END})

graph.add_edge("tools", "agent")

# 6. Compile the graph
app = graph.compile()

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What were the major developments in quantum computing in 2023?"
            }
        ],
        "research_needed": "",
        "research_subject": "",
        "research_year": None,
        "research_is_latest": False,
    }
)

print(result)
