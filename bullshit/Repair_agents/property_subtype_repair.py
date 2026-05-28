from typing import Optional, List

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

class PropertySubtypeRepairOutput(BaseModel):

    property_subtype: Optional[str] = None

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
    PropertySubtypeRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite property subtype repair agent.

Your ONLY task:
Repair incorrect property subtype extraction.

VALID PROPERTY TYPES:
- apartment
- flat
- villa
- penthouse
- duplex
- studio
- rk
- office
- shop
- showroom
- plot
- row house
- bungalow
- warehouse

STRICT RULES:
- Extract ONLY explicitly mentioned subtype
- NEVER infer aggressively
- Ignore furnishing
- Ignore amenities
- Ignore locality names

IMPORTANT:
- "1rk" or "rk" → rk
- "studio apartment" → studio
- "office space" → office
- "commercial shop" → shop

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT PROPERTY SUBTYPE:
{current_property_subtype}


VERIFIER ISSUE:
{issue}


Extract corrected property subtype.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_property_subtype_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "property_core_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:

        if item.get("field_name") == "property.property_subtype":

            if item.get("is_correct") is False:

                return item.get("issue")

    return None


# =========================================================
# NODE
# =========================================================

def repair_property_subtype_llm(state: GraphState):

    # =====================================================
    # CHECK FAILURE
    # =====================================================

    issue = get_property_subtype_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_property_subtype = state.property_subtype

    # =====================================================
    # INVOKE
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_property_subtype": str(
                current_property_subtype
            ),

            "issue": issue
        })

    except Exception as e:

        print("Property Subtype Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    repaired_subtype = response.property_subtype

    # =====================================================
    # NO VALUE FOUND
    # =====================================================

    if repaired_subtype is None:

        repair_result = RepairResult(

            field_name="property.property_subtype",

            old_value=current_property_subtype,

            new_value=None,

            confidence=response.confidence,

            is_repaired=False,

            evidence=response.evidence,

            issue=issue,

            repair_agent="property_subtype_llm_repair"
        )

        return {

            "repair_candidates": [

                repair_result.model_dump()
            ]
        }

    # =====================================================
    # NORMALIZATION
    # =====================================================

    repaired_subtype = (
        repaired_subtype
        .lower()
        .strip()
    )

    # =====================================================
    # VALID VALUES
    # =====================================================

    valid_values = {

        "apartment",
        "flat",
        "villa",
        "penthouse",
        "duplex",
        "studio",
        "rk",
        "office",
        "shop",
        "showroom",
        "plot",
        "row house",
        "bungalow",
        "warehouse"
    }

    if repaired_subtype not in valid_values:

        return {}

    # =====================================================
    # SAME VALUE
    # =====================================================

    if repaired_subtype == current_property_subtype:

        return {}

    # =====================================================
    # BUILD RESULT
    # =====================================================

    repair_result = RepairResult(

        field_name="property.property_subtype",

        old_value=current_property_subtype,

        new_value=repaired_subtype,

        confidence=response.confidence,

        is_repaired=True,

        evidence=response.evidence,

        issue=issue,

        repair_agent="property_subtype_llm_repair"
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "repair_candidates": [

            repair_result.model_dump()
        ]
    }