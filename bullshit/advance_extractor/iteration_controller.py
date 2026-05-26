from extractor.GraphState import GraphState


# ==========================================
# ITERATION CONTROLLER
# ==========================================

MAX_ITERATIONS = 3


def iteration_controller(state: GraphState):

    validation_report = state.get(
        "validation_report",
        {}
    )

    iteration_count = state.get(
        "iteration_count",
        0
    )

    verification_history = state.get(
        "verification_history",
        []
    )

    is_valid = validation_report.get(
        "is_valid",
        False
    )

    confidence_score = validation_report.get(
        "confidence_score",
        0
    )

    critical_issues = validation_report.get(
        "critical_issues",
        []
    )

    # ======================================
    # STORE HISTORY
    # ======================================

    verification_history.append({

        "iteration": iteration_count,

        "is_valid": is_valid,

        "confidence_score": confidence_score,

        "critical_issues": critical_issues
    })

    # ======================================
    # SUCCESS CONDITION
    # ======================================

    if is_valid:

        return {

            "should_continue": False,

            "verification_history": verification_history
        }

    # ======================================
    # MAX ITERATION LIMIT
    # ======================================

    if iteration_count >= MAX_ITERATIONS:

        return {

            "should_continue": False,

            "verification_history": verification_history
        }

    # ======================================
    # RETRY
    # ======================================

    return {

        "should_continue": True,

        "verification_history": verification_history
    }