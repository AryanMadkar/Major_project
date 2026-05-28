from extractor.GraphState import GraphState


# =========================================================
# NODE
# =========================================================

def increment_repair_iteration(state: GraphState):

    current = state.iteration_count or 0

    return {

        "iteration_count": current + 1
    }