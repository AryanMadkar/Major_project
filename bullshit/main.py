from langgraph.graph import StateGraph, END
import json

from extractor.GraphState import GraphState

# =========================================================
# EXTRACTORS
# =========================================================

from extractor.cleaned import clean_text_node
from extractor.Type import extract_type
from extractor.bhk import extract_bhk
from extractor.price_extractor import extract_price
from extractor.location_extractor import extract_location
from extractor.furnishing_extractor import extract_furnishing
from extractor.facing_extractor import extract_facing
from extractor.parking_extractor import extract_parking
from extractor.amenities_extractor import extract_amenities
from extractor.property_subtype_extractor import (
    extract_property_subtype
)
from extractor.metadata_extractor import extract_metadata

# =========================================================
# RESPONSE
# =========================================================

from extractor.Response import response_node

# =========================================================
# VERIFIERS
# =========================================================

from verifier.verify_property_core import (
    verify_property_core
)

from verifier.verify_financials import (
    verify_financials
)

from verifier.verify_contextual import (
    verify_contextual
)


# =========================================================
# REPAIR AGENTS
# =========================================================

from Repair_agents.bhk_repair import repair_bhk_llm

from Repair_agents.price_repair import repair_price_llm

from Repair_agents.request_type_repair import (
    repair_request_type_llm
)

from Repair_agents.property_subtype_repair import (
    repair_property_subtype_llm
)

from Repair_agents.location_repair import (
    repair_location_llm
)

from  Repair_agents.parking_repair import (
    repair_parking_llm
)

from  Repair_agents.furnishing_repair import (
    repair_furnishing_llm
)

from  Repair_agents.facing_repair import (
    repair_facing_llm
)

from repair.repair_cycle_controller import (
    repair_cycle_controller
)

from repair.increment_repair_iteration import (
    increment_repair_iteration
)

from repair.repair_router import repair_router
from repair.repair_dispatcher import repair_dispatcher
from repair.reverification_router import reverification_router

# =========================================================
# REPAIR ORCHESTRATION
# =========================================================

from repair.verification_aggregator import (
    verification_aggregator
)

from repair.apply_repairs import (
    apply_repairs
)

# =========================================================
# ROUTING FUNCTIONS
# =========================================================

def route_repair_agents(state: GraphState):
    failed = state.failed_fields or []
    attempts = state.repair_attempts or {}
    from repair.repair_dispatcher import FIELD_TO_AGENT
    
    agents = set()
    for field in failed:
        if attempts.get(field, 0) < 2:  # MAX_REPAIR_ATTEMPTS = 2
            agent = FIELD_TO_AGENT.get(field)
            if agent:
                agents.add(agent)
    return list(agents)

def route_verifiers(state: GraphState):
    if state.reverification_required is None:
        return ["verify_property_core", "verify_financials", "verify_contextual"]
    return reverification_router(state)

def combined_repair_router(state: GraphState):
    if (state.iteration_count or 0) >= 2:  # MAX_GLOBAL_REPAIR_CYCLES = 2
        return "finalize"
    route = repair_router(state)
    return "repair" if route == "repair" else "finalize"


# =========================================================
# GRAPH
# =========================================================

builder = StateGraph(GraphState)

# =========================================================
# ADD NODES
# =========================================================


builder.add_node(
    "clean_text",
    clean_text_node
)

builder.add_node(
    "extract_request_type",
    extract_type
)

builder.add_node(
    "extract_bhk",
    extract_bhk
)

builder.add_node(
    "extract_price",
    extract_price
)

builder.add_node(
    "extract_location",
    extract_location
)

builder.add_node(
    "extract_furnishing",
    extract_furnishing
)

builder.add_node(
    "extract_facing",
    extract_facing
)

builder.add_node(
    "extract_parking",
    extract_parking
)

builder.add_node(
    "extract_amenities",
    extract_amenities
)

builder.add_node(
    "extract_property_subtype",
    extract_property_subtype
)

builder.add_node(
    "extract_metadata",
    extract_metadata
)

builder.add_node(
    "response",
    response_node
)

# =========================================================
# REPAIR AGENTS
# =========================================================

builder.add_node(
    "repair_bhk",
    repair_bhk_llm
)

builder.add_node(
    "repair_price",
    repair_price_llm
)

builder.add_node(
    "repair_request_type",
    repair_request_type_llm
)

builder.add_node(
    "repair_property_subtype",
    repair_property_subtype_llm
)

builder.add_node(
    "repair_location",
    repair_location_llm
)

builder.add_node(
    "repair_parking",
    repair_parking_llm
)

builder.add_node(
    "repair_furnishing",
    repair_furnishing_llm
)

builder.add_node(
    "repair_facing",
    repair_facing_llm
)

# =========================================================
# ORCHESTRATION
# =========================================================

builder.add_node(
    "verification_aggregator",
    verification_aggregator
)

builder.add_node(
    "apply_repairs",
    apply_repairs
)

builder.add_node(
    "repair_dispatcher",
    repair_dispatcher
)

# =========================================================
# VERIFICATION NODES
# =========================================================

builder.add_node(
    "verify_property_core",
    verify_property_core
)

builder.add_node(
    "verify_financials",
    verify_financials
)

builder.add_node(
    "repair_cycle_controller",
    lambda state: {}
)

builder.add_node(
    "increment_repair_iteration",
    increment_repair_iteration
)
builder.add_node(
    "verify_contextual",
    verify_contextual
)

# =========================================================
# ENTRY POINT
# =========================================================

builder.set_entry_point("clean_text")

# =========================================================
# EXTRACTION FLOW
# =========================================================

builder.add_edge(
    "clean_text",
    "extract_request_type"
)

builder.add_edge(
    "clean_text",
    "extract_bhk"
)

builder.add_edge(
    "clean_text",
    "extract_location"
)

builder.add_edge(
    "clean_text",
    "extract_furnishing"
)

builder.add_edge(
    "clean_text",
    "extract_facing"
)

builder.add_edge(
    "clean_text",
    "extract_parking"
)

builder.add_edge(
    "clean_text",
    "extract_amenities"
)

builder.add_edge(
    "clean_text",
    "extract_property_subtype"
)

# =========================================================
# PRICE DEPENDS ON REQUEST TYPE
# =========================================================

builder.add_edge(
    "extract_request_type",
    "extract_price"
)

# =========================================================
# METADATA WAITS FOR ALL EXTRACTIONS
# =========================================================

builder.add_edge(
    [
        "extract_request_type",
        "extract_bhk",
        "extract_price",
        "extract_location",
        "extract_furnishing",
        "extract_facing",
        "extract_parking",
        "extract_amenities",
        "extract_property_subtype"
    ],
    "extract_metadata"
)

# =========================================================
# RESPONSE NODE
# =========================================================

builder.add_edge(
    "extract_metadata",
    "response"
)

# =========================================================
# PARALLEL VERIFICATION & LOCALIZED REVERIFICATION
# =========================================================

builder.add_conditional_edges(
    "response",
    route_verifiers,
    {
        "verify_property_core": "verify_property_core",
        "verify_financials": "verify_financials",
        "verify_contextual": "verify_contextual"
    }
)

# =========================================================
# END (Separate edges to support dynamic skipped nodes in join)
# =========================================================

builder.add_edge("verify_property_core", "verification_aggregator")
builder.add_edge("verify_financials", "verification_aggregator")
builder.add_edge("verify_contextual", "verification_aggregator")

# =========================================================
# PARALLEL REPAIR EXECUTION
# =========================================================

builder.add_edge(
    "repair_bhk",
    "apply_repairs"
)

builder.add_edge(
    "repair_price",
    "apply_repairs"
)

builder.add_edge(
    "repair_request_type",
    "apply_repairs"
)

builder.add_edge(
    "repair_property_subtype",
    "apply_repairs"
)

builder.add_edge(
    "repair_location",
    "apply_repairs"
)

builder.add_edge(
    "repair_parking",
    "apply_repairs"
)

builder.add_edge(
    "repair_furnishing",
    "apply_repairs"
)

builder.add_edge(
    "repair_facing",
    "apply_repairs"
)


# =========================================================
# REVERIFY (via response to rebuild output)
# =========================================================

builder.add_edge(
    "apply_repairs",
    "response"
)

# =========================================================
# FINAL RESPONSE
# =========================================================

builder.add_edge(
    "verification_aggregator",
    "repair_cycle_controller"
)

builder.add_conditional_edges(

    "repair_cycle_controller",

    combined_repair_router,

    {

        "repair":
            "increment_repair_iteration",

        "finalize":
            END
    }
)

# =========================================================
# DYNAMIC REPAIR DISPATCHING
# =========================================================

builder.add_edge(
    "increment_repair_iteration",
    "repair_dispatcher"
)

builder.add_conditional_edges(
    "repair_dispatcher",
    route_repair_agents,
    {
        "repair_bhk": "repair_bhk",
        "repair_price": "repair_price",
        "repair_request_type": "repair_request_type",
        "repair_property_subtype": "repair_property_subtype",
        "repair_location": "repair_location",
        "repair_parking": "repair_parking",
        "repair_furnishing": "repair_furnishing",
        "repair_facing": "repair_facing"
    }
)




# =========================================================
# COMPILE
# =========================================================

graph = builder.compile()

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    png_data = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png_data)

    result = graph.invoke({

        "user_input": """
🏠 REQUIRED 1 BHK FLAT FOR OUT RATE
BUDGET 1 CR TO 1.10 CR

LOCATION ANY CHARKOP SECTOR
KANDIVALI WEST

Big swimming pool
inbuild gym

CALL
9820067788

CONTACT PERSON SURESH
"""
    })

    structured_output = result.get(
        "response_output"
    )

    validation_report = result.get(
        "validation_report"
    )

    print("\nFinal Structured Output:\n")

    print(
        json.dumps(
            structured_output,
            indent=2,
            ensure_ascii=False
        )
    )

    print("\nValidation Report:\n")

    print(
        json.dumps(
            validation_report,
            indent=2,
            ensure_ascii=False
        )
    )
