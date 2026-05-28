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

class ParkingRepairOutput(BaseModel):

    parking_count: Optional[int] = None

    parking_type: Optional[str] = None

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
    ParkingRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite parking repair agent.

Your ONLY task:
Repair incorrect parking extraction.

STRICT RULES:
- Extract ONLY explicit parking details
- NEVER infer
- Ignore prices
- Ignore BHK
- Ignore phone numbers
- Ignore sqft/area

VALID PARKING TYPES:
- covered
- open
- stilt
- car

IMPORTANT:
- "parking available" can mean parking_count=1
- Only assign parking_type if explicit
- Ignore unrelated numbers

VALID:
- 2 car parking
- covered parking
- parking available
- stilt parking

INVALID:
- 2 bhk
- 2 lakh
- 2 cr
- 2 bathrooms

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT PARKING COUNT:
{current_parking_count}


CURRENT PARKING TYPE:
{current_parking_type}


VERIFIER ISSUE:
{issue}


Extract corrected parking details.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_parking_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "financial_verification",
        {}
    )

    results = section.get("results", [])

    failed_issues = []

    for item in results:

        if item.get("field_name") in {

            "parking.parking_count",
            "parking.parking_type"
        }:

            if item.get("is_correct") is False:

                issue = item.get("issue")

                if issue:
                    failed_issues.append(issue)

    if not failed_issues:
        return None

    return " | ".join(failed_issues)


# =========================================================
# NODE
# =========================================================

def repair_parking_llm(state: GraphState):

    # =====================================================
    # CHECK FAILURE
    # =====================================================

    issue = get_parking_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_parking_count = state.parking_count

    current_parking_type = state.parking_type

    # =====================================================
    # INVOKE
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_parking_count":
                str(current_parking_count),

            "current_parking_type":
                str(current_parking_type),

            "issue": issue
        })

    except Exception as e:

        print("Parking Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    repaired_count = response.parking_count

    repaired_type = response.parking_type

    # =====================================================
    # NORMALIZATION
    # =====================================================

    if repaired_type:

        repaired_type = (
            repaired_type
            .lower()
            .strip()
        )

    # =====================================================
    # NO DATA FOUND
    # =====================================================

    if repaired_count is None and repaired_type is None:

        return {

            "repair_candidates": [

                RepairResult(

                    field_name="parking.parking_count",

                    old_value=current_parking_count,

                    new_value=None,

                    confidence=response.confidence,

                    is_repaired=False,

                    evidence=response.evidence,

                    issue=issue,

                    repair_agent="parking_llm_repair"

                ).model_dump()
            ]
        }

    # =====================================================
    # BUILD CANDIDATES
    # =====================================================

    repair_candidates = []

    # =====================================================
    # COUNT
    # =====================================================

    if repaired_count != current_parking_count:

        repair_candidates.append(

            RepairResult(

                field_name="parking.parking_count",

                old_value=current_parking_count,

                new_value=repaired_count,

                confidence=response.confidence,

                is_repaired=True,

                evidence=response.evidence,

                issue=issue,

                repair_agent="parking_llm_repair"

            ).model_dump()
        )

    # =====================================================
    # TYPE
    # =====================================================

    if repaired_type != current_parking_type:

        repair_candidates.append(

            RepairResult(

                field_name="parking.parking_type",

                old_value=current_parking_type,

                new_value=repaired_type,

                confidence=response.confidence,

                is_repaired=True,

                evidence=response.evidence,

                issue=issue,

                repair_agent="parking_llm_repair"

            ).model_dump()
        )

    # =====================================================
    # RETURN
    # =====================================================

    if not repair_candidates:

        return {}

    return {

        "repair_candidates": repair_candidates
    }