from extractor.GraphState import GraphState


# ==========================================
# ITERATION CONTROLLER
# ==========================================

MAX_ITERATIONS = 3


def iteration_controller(state: GraphState):

    validation_report = state.validation_report or {}

    iteration_count = state.iteration_count or 0

    verification_history = list(state.verification_history or [])

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