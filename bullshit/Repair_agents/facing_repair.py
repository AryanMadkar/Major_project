from typing import Optional

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

from extractor.GraphState import GraphState

from repair.base_repair import RepairResult


load_dotenv()


# =========================================================
# STRUCTURED OUTPUT
# =========================================================

class FacingRepairOutput(BaseModel):

    facing: Optional[str] = None

    confidence: int = Field(
        ge=0,
        le=100
    )

    evidence: Optional[str] = None


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(
    FacingRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite facing direction repair agent.

Your ONLY task:
Repair incorrect facing extraction.

VALID VALUES:
- north
- south
- east
- west
- north_east
- north_west
- south_east
- south_west

STRICT RULES:
- Extract ONLY explicit facing directions
- NEVER infer
- Ignore locality names
- Ignore amenities
- Ignore prices
- Ignore furnishing

IMPORTANT:
- "north east facing" → north_east
- "ne facing" → north_east
- "south west facing" → south_west
- "east facing flat" → east

INVALID:
- east and west ventilation
- north side balcony
- west open view

Direction must explicitly refer to property facing.

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT FACING:
{current_facing}


VERIFIER ISSUE:
{issue}


Extract corrected facing direction.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_facing_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "contextual_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:

        if item.get("field_name") == "attributes.facing":

            if item.get("is_correct") is False:

                return item.get("issue")

    return None


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_facing(value):

    if not value:
        return None

    value = value.lower().strip()

    mapping = {

        "north": "north",
        "south": "south",
        "east": "east",
        "west": "west",

        "north east": "north_east",
        "north-east": "north_east",
        "northeast": "north_east",
        "ne": "north_east",

        "north west": "north_west",
        "north-west": "north_west",
        "northwest": "north_west",
        "nw": "north_west",

        "south east": "south_east",
        "south-east": "south_east",
        "southeast": "south_east",
        "se": "south_east",

        "south west": "south_west",
        "south-west": "south_west",
        "southwest": "south_west",
        "sw": "south_west",
    }

    return mapping.get(value)


# =========================================================
# NODE
# =========================================================

def repair_facing_llm(state: GraphState):

    # =====================================================
    # CHECK FAILURE
    # =====================================================

    issue = get_facing_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_facing = state.facing

    # =====================================================
    # INVOKE
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_facing":
                str(current_facing),

            "issue": issue
        })

    except Exception as e:

        print("Facing Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    repaired_facing = normalize_facing(
        response.facing
    )

    # =====================================================
    # NO VALUE FOUND
    # =====================================================

    if repaired_facing is None:

        return {

            "repair_candidates": [

                RepairResult(

                    field_name="attributes.facing",

                    old_value=current_facing,

                    new_value=None,

                    confidence=response.confidence,

                    is_repaired=False,

                    evidence=response.evidence,

                    issue=issue,

                    repair_agent="facing_llm_repair"

                ).model_dump()
            ]
        }

    # =====================================================
    # SAME VALUE
    # =====================================================

    if repaired_facing == current_facing:

        return {}

    # =====================================================
    # BUILD RESULT
    # =====================================================

    repair_result = RepairResult(

        field_name="attributes.facing",

        old_value=current_facing,

        new_value=repaired_facing,

        confidence=response.confidence,

        is_repaired=True,

        evidence=response.evidence,

        issue=issue,

        repair_agent="facing_llm_repair"
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "repair_candidates": [

            repair_result.model_dump()
        ]
    }