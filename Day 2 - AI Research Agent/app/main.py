from typing import Literal, TypedDict
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from urllib3 import response
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from tools import calculator

load_dotenv()


# 1. Define the graph's state
class State(TypedDict):
    question: str
    answer: str
    complexity: str
    isToolNeeded: str

class Classification(BaseModel):
    complexity: Literal["simple", "complex"] = Field (
        description="Whether the question is simple or complex"
    )
    
 
class ToolClassification(BaseModel):
    isToolNeeded: Literal["yes", "no"] = Field (
        description="Whether the question is an arithemetic problem"
    )

# Create LLM node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

classifier_llm = llm.with_structured_output(Classification)
tool_classifier_llm  = llm.with_structured_output(ToolClassification)

llm_with_tools = llm.bind_tools([calculator])


def classify_question(state: State):
    question = state["question"]

    response = classifier_llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "Classify the user's question as either "
                    "'simple' or 'complex'. "
                    "Return only one word: simple or complex."
                ),
            },
            {"role": "user", "content": question},
        ]
    )

    return {"complexity": response.complexity}


def direct_answer(state: State):
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant helping a developer "
                    "learn about AI, LLMs, and software engineering."
                ),
            },
            {"role": "user", "content": state["question"]},
        ]
    )

    return {"answer": response.content.strip().lower()}


def research(state: State):
    return {
        "answer": (
            "This question was classified as complex. "
            "A research workflow would happen here."
        )
    }


def route_question(state: State):
    if state["complexity"] == "simple":
        return "tool_needed"

    return "research"

def tool_routing(state: State):
    if state["isToolNeeded"] == "yes":
        return "calculator"
    return "direct_answer"

def calculator_node(state: State):
    tool_call_response = llm_with_tools.invoke(
        state["question"]
    )

    if tool_call_response.tool_calls[0]:
        tool_call = tool_call_response.tool_calls[0]
 
        tool_result = calculator.invoke(tool_call["args"])

        return {
            "answer": str(tool_result)
        }

    return {
        "answer": tool_call_response.content
    }

def tool_decision(state: State):
    question = state["question"]

    response = tool_classifier_llm.invoke([
        {
            "role": "system",
            "content": "Classify the user's question as either "
                    "arithemtic or not. "
                    "Return only one word: 'yes' if arithemetic or 'no' if not arithmetic."
        },
        {
            "role": "user",
            "content": question
        }
    ])

    return {"isToolNeeded": response.isToolNeeded}


# 3. Create the graph
graph = StateGraph(State)

# 4. Add a node
graph.add_node("classify_question", classify_question)
graph.add_node("direct_answer", direct_answer)
graph.add_node("research", research)
graph.add_node("calculator", calculator_node)
graph.add_node("tool_needed", tool_decision)


# 4. Define the workflow
graph.add_edge(START, "classify_question")

graph.add_conditional_edges(
    "classify_question",
    route_question,
    {
        "tool_needed": "tool_needed",
        "research": "research",
    },
)

graph.add_conditional_edges(
    "tool_needed",
    tool_routing,
    {
        "calculator" : "calculator",
        "direct_answer": "direct_answer"
    }
)

graph.add_edge("calculator", END)
graph.add_edge("direct_answer", END)
graph.add_edge("research", END)


# graph.add_edge("ask_llm", END)

# 6. Compile the graph
app = graph.compile()

# 7. Run the graph
result = app.invoke(
    {"question": "What is 44*891?", "answer": "", "complexity": "", "isToolNeeded": ""}
)

print(result)
