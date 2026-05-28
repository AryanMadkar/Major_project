import copy
from extractor.GraphState import GraphState
from extractor.Response import FinalOutput, build_traceable_meta

MAX_ITERATIONS = 3


def iteration_controller(state: GraphState):
    """
    Tracks iterations and finalizes timing and metadata when ending execution.
    """


    validation_report = state.validation_report or {}
    iteration_count = state.iteration_count or 0
    verification_history = list(state.verification_history or [])

    is_valid = validation_report.get("is_valid", False)
    confidence_score = validation_report.get("confidence_score", 0)
    critical_issues = validation_report.get("critical_issues", [])

    verification_history.append({
        "iteration": iteration_count,
        "is_valid": is_valid,
        "confidence_score": confidence_score,
        "critical_issues": critical_issues
    })

    # Determine continuation
    should_continue = True
    if is_valid or iteration_count >= MAX_ITERATIONS:
        should_continue = False



    response_output = copy.deepcopy(state.response_output or {})

    # Finalize response output if we are ending
    if not should_continue:
        # Re-compile traceable metadata with updated fields & repair history
        response_output["extraction_meta"] = {
            "summary.request_type": build_traceable_meta("summary.request_type", "keyword+rules", 90, state.request_type, state),
            "summary.bhk": build_traceable_meta("summary.bhk", "regex", 90, state.bhk, state),
            "pricing.price": build_traceable_meta("pricing.price", "regex+rules", 85, state.price, state),
            "pricing.price_min": build_traceable_meta("pricing.price_min", "regex+rules", 85, state.price_min, state),
            "pricing.price_max": build_traceable_meta("pricing.price_max", "regex+rules", 85, state.price_max, state),
            "pricing.rent_price": build_traceable_meta("pricing.rent_price", "regex+rules", 90, state.rent_price, state),
            "pricing.deposit_price": build_traceable_meta("pricing.deposit_price", "regex+rules", 90, state.deposit_price, state),
            "location.primary_location": build_traceable_meta("location.primary_location", "dictionary+patterns", 80, state.primary_location, state),
            "location.locations": build_traceable_meta("location.locations", "dictionary+patterns", 80, state.locations, state),
            "location.railway_line": build_traceable_meta("location.railway_line", "dictionary", 85, state.railway_line, state),
            "attributes.furnishing": build_traceable_meta("attributes.furnishing", "keyword+scoring", 80, state.furnishing, state),
            "attributes.facing": build_traceable_meta("attributes.facing", "keyword", 85, state.facing, state),
            "parking.parking_count": build_traceable_meta("parking.parking_count", "regex", 80, state.parking_count, state),
            "parking.parking_type": build_traceable_meta("parking.parking_type", "keyword", 80, state.parking_type, state),
            "amenities": build_traceable_meta("amenities", "regex+llm", 75, state.amenities, state),
            "property.property_subtype": build_traceable_meta("property.property_subtype", "keyword+llm", 80, state.property_subtype, state),
            "property.all_detected_subtypes": build_traceable_meta("property.all_detected_subtypes", "keyword+llm", 75, state.all_detected_subtypes, state),
            "metadata.message_title": build_traceable_meta("metadata.message_title", "llm+rules", 75, state.message_title, state),
            "metadata.contact_people": build_traceable_meta("metadata.contact_people", "llm+cleanup", 85, state.contact_people, state),
            "metadata.contact_numbers": build_traceable_meta("metadata.contact_numbers", "regex+llm", 95, state.contact_numbers, state),
        }



        # Enforce Final Schema validation
        try:
            FinalOutput.model_validate(response_output)
        except Exception as e:
            print("Final Output Schema Validation Error:", e)

    return {
        "should_continue": should_continue,
        "verification_history": verification_history,
        "response_output": response_output,
    }