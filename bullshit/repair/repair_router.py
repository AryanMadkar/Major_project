from extractor.GraphState import GraphState


MAX_REPAIR_ATTEMPTS = 2


# =========================================================
# ROUTER
# =========================================================

def repair_router(state: GraphState):

    failed_fields = (
        state.failed_fields or []
    )

    if not failed_fields:

        return "end"

    attempts = (
        state.repair_attempts or {}
    )

    retryable_fields = []

    for field in failed_fields:

        count = attempts.get(field, 0)

        if count < MAX_REPAIR_ATTEMPTS:

            retryable_fields.append(field)

    if not retryable_fields:

        return "end"

    return "repair"