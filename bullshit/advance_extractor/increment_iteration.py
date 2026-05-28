from extractor.GraphState import GraphState


def increment_iteration(state: GraphState):
    """
    Increments iteration counter and records timing.
    """


    current = state.iteration_count or 0
    new_iteration = current + 1

    return {
        "iteration_count": new_iteration,
    }