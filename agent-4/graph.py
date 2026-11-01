from state import AgentState

from agents.researcher import researcher
from agents.analyst import analyze
from agents.validator import validate
from agents.synthesizer import synthesize

from langgraph.graph import StateGraph, START, END

MAX_RECOVERY_ATTEMPTS = 2


async def researcher_node(state: AgentState) -> dict:
    user_question = state["user_question"]
    validation = state["validation_result"]

    if validation and validation["missing_information"]:
        missing = "\n".join(f"-{item}" for item in validation["missing_information"])

        research_question = (
            f"{user_question}\n\n"
            "Follow-up research must address these gaps:\n"
            f"{missing}"
        )
    else:
        research_question = user_question

    old_results = state["research_results"]
    new_results = await researcher(research_question)

    results = {
        **old_results,
        **new_results
    }

    return {"research_results": results}


async def analyst_node(state: AgentState) -> dict:

    user_question = state["user_question"]
    validation = state["validation_result"]

    if validation and not validation["is_valid"]:
        feedback = (
            f"\n\nPrevious validation feedback:\n"
            f"Reason: {validation['reason']}\n"
            f"Missing information: {validation['missing_information']}\n"
            "Reassess the existing evidence and address this feedbacl. "
            "Do not invent evidence or claim unsupported conclusions."
        )

        user_question = user_question + feedback

    analysis_result = await analyze(
        user_question=user_question, research_results=state["research_results"]
    )

    # Using mode_dump() to convert the Pydantic type to a dictionary type.
    return {"analysis": analysis_result.model_dump()}


async def validator_node(state: AgentState) -> dict:
    validation_result = await validate(
        user_question=state["user_question"],
        analysis=state["analysis"],
        research_results=state["research_results"],
    )

    return {
        "validation_result": validation_result.model_dump(),
        "validation_attempts": state["validation_attempts"] + 1,
    }


async def syntesizer_node(state: AgentState) -> dict:
    synthesized_result = await synthesize(
        user_question=state["user_question"],
        research_results=state["research_results"],
        analysis=state["analysis"],
        validation_result=state["validation_result"],
    )

    return {"final_answer": synthesized_result.model_dump()}


# logic based routing functions


def route_after_validation(state: AgentState) -> str:
    validation = state["validation_result"]

    print("Validation attempts:", state["validation_attempts"])
    print("Is valid:", validation["is_valid"])
    print("Missing information:", validation["missing_information"])

    if validation["is_valid"]:
        return "synthesizer"

    if state["validation_attempts"] >= MAX_RECOVERY_ATTEMPTS + 1:
        return "synthesizer"

    return "recovery"


def route_recovery(state: AgentState) -> str:
    validation = state["validation_result"]

    if validation["missing_information"]:
        return "researcher"

    return "analyst"


# Define a graph instance


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("researcher", researcher_node)
    builder.add_node("analyst", analyst_node)
    builder.add_node("validator", validator_node)
    builder.add_node("synthesizer", syntesizer_node)
    builder.add_node("recovery_router", lambda state: {})

    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "analyst")
    builder.add_edge("analyst", "validator")
    builder.add_conditional_edges(
        "validator",
        route_after_validation,
        {"synthesizer": "synthesizer", "recovery": "recovery_router"},
    )
    builder.add_conditional_edges(
        "recovery_router",
        route_recovery,
        {"researcher": "researcher", "analyst": "analyst"},
    )

    builder.add_edge("synthesizer", END)

    return builder.compile()
