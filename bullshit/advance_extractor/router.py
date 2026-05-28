from extractor.GraphState import GraphState


# ==========================================
# RETRY ROUTER
# ==========================================

def retry_router(state: GraphState):

    should_continue = state.should_continue or False

    if should_continue:

        return "retry"

    return "end"