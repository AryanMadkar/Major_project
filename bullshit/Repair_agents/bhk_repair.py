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

class BHKRepairOutput(BaseModel):

    bhk: Optional[int] = None

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
    BHKRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite BHK repair agent.

Your ONLY task:
Repair incorrect BHK extraction.

STRICT RULES:
- Extract ONLY explicit BHK values
- NEVER infer
- Ignore prices
- Ignore phone numbers
- Ignore parking counts
- Ignore sqft/area values

VALID EXAMPLES:
- 2bhk
- 2 bhk
- 3-bhk
- two bhk
- 2 bedroom

INVALID:
- 2 parking
- 2 lakh
- 2 cr
- 200 sqft

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT EXTRACTED BHK:
{current_bhk}


VERIFIER ISSUE:
{issue}


Extract corrected BHK.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_bhk_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "property_core_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:

        if item.get("field_name") == "summary.bhk":

            if item.get("is_correct") is False:

                return item.get("issue")

    return None


# =========================================================
# NODE
# =========================================================

def repair_bhk_llm(state: GraphState):

    # =====================================================
    # CHECK IF BHK FAILED
    # =====================================================

    issue = get_bhk_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_bhk = state.bhk

    # =====================================================
    # INVOKE LLM
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_bhk": str(current_bhk),

            "issue": issue
        })

    except Exception as e:

        print("BHK Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    # =====================================================
    # VALIDATION
    # =====================================================

    repaired_bhk = response.bhk

    if repaired_bhk is None:

        return {}

    if repaired_bhk == current_bhk:

        return {}

    # =====================================================
    # BUILD REPAIR RESULT
    # =====================================================

    repair_result = RepairResult(

        field_name="summary.bhk",

        old_value=current_bhk,

        new_value=repaired_bhk,

        confidence=response.confidence,

        is_repaired=True,

        evidence=response.evidence,

        issue=issue,

        repair_agent="bhk_llm_repair"
    )

    # =====================================================
    # RETURN REPAIR CANDIDATE
    # =====================================================

    return {

        "repair_candidates": [

            repair_result.model_dump()
        ]
    }