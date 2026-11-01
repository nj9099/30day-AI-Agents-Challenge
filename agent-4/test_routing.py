
from graph import route_after_validation, route_recovery, MAX_RECOVERY_ATTEMPTS

def make_state(is_valid, attempts, missing_information):
    return {
        "user_question": "What were the major advances in quantum computing in 2024?",
        "research_results": {},
        "analysis": {},
        "validation_result": {
            "is_valid": is_valid,
            "reason": "Test reason",
            "missing_information": missing_information,
        },
        "final_answer": None,
        "validation_attempts": attempts,
    }


# Test 1: Valid evidence should go to synthesis
state = make_state(True, 1, [])
assert route_after_validation(state) == "synthesizer"

# Test 2: Invalid evidence with retries remaining should enter recovery
state = make_state(False, 1, ["Evidence about error correction is missing"])
assert route_after_validation(state) == "recovery"

# Test 3: Exhausted retry budget should go to synthesis
state = make_state(False, MAX_RECOVERY_ATTEMPTS + 1, ["Evidence is missing"])
assert route_after_validation(state) == "synthesizer"

# Test 4: Missing information should trigger research
state = make_state(False, 1, ["Evidence about error correction is missing"])
assert route_recovery(state) == "researcher"

# Test 5: No listed missing information should trigger reanalysis
state = make_state(False, 1, [])
assert route_recovery(state) == "analyst"

print("All routing tests passed!")
