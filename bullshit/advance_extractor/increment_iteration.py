from extractor.GraphState import GraphState


# ==========================================
# ITERATION COUNTER
# ==========================================

def increment_iteration(state: GraphState):

    current = state.iteration_count or 0

    return {

        "iteration_count": current + 1
    }