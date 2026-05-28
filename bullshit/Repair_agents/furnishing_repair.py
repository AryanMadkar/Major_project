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

class FurnishingRepairOutput(BaseModel):

    furnishing: Optional[str] = None

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
    FurnishingRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite furnishing repair agent.

Your ONLY task:
Repair incorrect furnishing extraction.

VALID VALUES:
- fully_furnished
- semi_furnished
- unfurnished

STRICT RULES:
- Extract ONLY furnishing information
- NEVER infer aggressively
- Ignore amenities
- Ignore prices
- Ignore locality names

FULLY FURNISHED:
- fully furnished
- luxury furnished
- complete furnished

SEMI FURNISHED:
- semi furnished
- wardrobe
- modular kitchen
- geyser
- ac fitted

UNFURNISHED:
- unfurnished
- bare flat
- empty flat

IMPORTANT:
- Furnished clues must be explicit
- Do not assume AC means fully furnished

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT FURNISHING:
{current_furnishing}


VERIFIER ISSUE:
{issue}


Extract corrected furnishing.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_furnishing_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "contextual_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:

        if item.get("field_name") == "attributes.furnishing":

            if item.get("is_correct") is False:

                return item.get("issue")

    return None


# =========================================================
# NODE
# =========================================================

def repair_furnishing_llm(state: GraphState):

    # =====================================================
    # CHECK FAILURE
    # =====================================================

    issue = get_furnishing_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_furnishing = state.furnishing

    # =====================================================
    # INVOKE
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_furnishing":
                str(current_furnishing),

            "issue": issue
        })

    except Exception as e:

        print("Furnishing Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    repaired_furnishing = response.furnishing

    # =====================================================
    # NORMALIZATION
    # =====================================================

    if repaired_furnishing:

        repaired_furnishing = (
            repaired_furnishing
            .lower()
            .strip()
        )

    # =====================================================
    # VALID VALUES
    # =====================================================

    valid_values = {

        "fully_furnished",
        "semi_furnished",
        "unfurnished"
    }

    if (
        repaired_furnishing is not None
        and repaired_furnishing not in valid_values
    ):

        return {}

    # =====================================================
    # NO VALUE FOUND
    # =====================================================

    if repaired_furnishing is None:

        return {

            "repair_candidates": [

                RepairResult(

                    field_name="attributes.furnishing",

                    old_value=current_furnishing,

                    new_value=None,

                    confidence=response.confidence,

                    is_repaired=False,

                    evidence=response.evidence,

                    issue=issue,

                    repair_agent="furnishing_llm_repair"

                ).model_dump()
            ]
        }

    # =====================================================
    # SAME VALUE
    # =====================================================

    if repaired_furnishing == current_furnishing:

        return {}

    # =====================================================
    # BUILD RESULT
    # =====================================================

    repair_result = RepairResult(

        field_name="attributes.furnishing",

        old_value=current_furnishing,

        new_value=repaired_furnishing,

        confidence=response.confidence,

        is_repaired=True,

        evidence=response.evidence,

        issue=issue,

        repair_agent="furnishing_llm_repair"
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "repair_candidates": [

            repair_result.model_dump()
        ]
    }