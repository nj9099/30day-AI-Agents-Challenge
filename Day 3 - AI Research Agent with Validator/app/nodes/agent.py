from state import State

from config.llm import llm_with_tools

def agent(state: State):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}

