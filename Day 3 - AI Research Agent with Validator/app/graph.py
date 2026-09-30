from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode


from state import State

from nodes.agent import agent
from nodes.research import research
from nodes.research_decision import research_decision
from nodes.validation import validate_research
from nodes.research_synthesis import research_synthesis
from nodes.refinement import refine_research_query
from nodes.query_check import check_research_query

from tools.research_tools import (
    calculator,
    word_counter,
    research_topic,
)

tool_node = ToolNode([calculator, word_counter, research_topic])

def route_tools(state: State):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


def route_research(state: State):
    if state["research_needed"] == "yes":
        return "research"
    return "agent"

def route_validation(state: State):
    if state["research_valid"]:
        return "synthesis"

    if state["research_attempts"] < 2:
        return "retry"

    return "terminate"

def route_query_check(state: State):
    if state["research_query_repeated"]:
        return END

    return "research"

# 3. Create the graph

def build_graph():

    graph = StateGraph(State)

    graph.add_node("agent", agent)
    graph.add_node("tools", tool_node)
    graph.add_node("research", research)
    graph.add_node("research_decision", research_decision)
    graph.add_node("research_synthesis", research_synthesis)
    graph.add_node("validate_research", validate_research)
    graph.add_node("refine_research_query", refine_research_query)
    graph.add_node("check_research_query", check_research_query)

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
        {
            "synthesis": "research_synthesis", 
            "retry": "refine_research_query",
            "terminate": "research_synthesis"
        },
    )
    graph.add_edge("refine_research_query", "check_research_query")

    graph.add_conditional_edges(
    "check_research_query",
    route_query_check,
    {
        "research": "research",
        END: END,
    },
)
    graph.add_edge("research_synthesis", END)


    # 6. Compile the graph
    app = graph.compile()

    return app
