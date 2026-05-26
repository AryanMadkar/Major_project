from extractor.GraphState import GraphState


# ==========================================
# RETRY ROUTER
# ==========================================

def retry_router(state: GraphState):

    should_continue = state.get(
        "should_continue",
        False
    )

    if should_continue:

        return "retry"

    return "end"