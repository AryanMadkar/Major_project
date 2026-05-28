from extractor.GraphState import GraphState


MAX_GLOBAL_REPAIR_CYCLES = 2


# =========================================================
# CONTROLLER
# =========================================================

def repair_cycle_controller(state: GraphState):

    # =====================================================
    # CURRENT ITERATION
    # =====================================================

    current_iteration = (
        state.iteration_count or 0
    )

    # =====================================================
    # FAILED FIELDS
    # =====================================================

    failed_fields = (
        state.failed_fields or []
    )

    # =====================================================
    # NO FAILURES
    # =====================================================

    if not failed_fields:

        return "finalize"

    # =====================================================
    # MAX ITERATIONS REACHED
    # =====================================================

    if current_iteration >= MAX_GLOBAL_REPAIR_CYCLES:

        return "finalize"

    # =====================================================
    # CONTINUE REPAIR
    # =====================================================

    return "repair"