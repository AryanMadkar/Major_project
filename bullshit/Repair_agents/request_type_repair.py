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

class RequestTypeRepairOutput(BaseModel):

    request_type: Optional[str] = None

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
    RequestTypeRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite real-estate request type repair agent.

Your ONLY task:
Repair incorrect request type extraction.

VALID VALUES:
- sale
- rent
- requirement

STRICT RULES:
- Return ONLY one valid request type
- NEVER infer aggressively
- Use explicit context only

SALE INDICATORS:
- sale
- selling
- outright
- purchase
- buy
- cr
- crore
- possession
- ownership

RENT INDICATORS:
- rent
- rental
- lease
- tenant
- monthly
- deposit

REQUIREMENT INDICATORS:
- wanted
- looking for
- requirement
- need flat
- searching for

IMPORTANT:
- If message is asking for property → requirement
- If message is offering property for rent → rent
- If message is offering property for sale → sale

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT REQUEST TYPE:
{current_request_type}


VERIFIER ISSUE:
{issue}


Extract corrected request type.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_request_type_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "property_core_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:

        if item.get("field_name") == "summary.request_type":

            if item.get("is_correct") is False:

                return item.get("issue")

    return None


# =========================================================
# NODE
# =========================================================

def repair_request_type_llm(state: GraphState):

    # =====================================================
    # CHECK IF FAILED
    # =====================================================

    issue = get_request_type_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_request_type = state.request_type

    # =====================================================
    # INVOKE LLM
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_request_type": str(current_request_type),

            "issue": issue
        })

    except Exception as e:

        print("Request Type Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY RESPONSE
    # =====================================================

    if response is None:

        return {}

    repaired_request_type = response.request_type

    # =====================================================
    # NO VALUE FOUND
    # =====================================================

    if repaired_request_type is None:

        repair_result = RepairResult(

            field_name="summary.request_type",

            old_value=current_request_type,

            new_value=None,

            confidence=response.confidence,

            is_repaired=False,

            evidence=response.evidence,

            issue=issue,

            repair_agent="request_type_llm_repair"
        )

        return {

            "repair_candidates": [

                repair_result.model_dump()
            ]
        }

    # =====================================================
    # INVALID VALUE SAFETY
    # =====================================================

    valid_values = {
        "sale",
        "rent",
        "requirement"
    }

    repaired_request_type = repaired_request_type.lower().strip()

    if repaired_request_type not in valid_values:

        return {}

    # =====================================================
    # SAME VALUE
    # =====================================================

    if repaired_request_type == current_request_type:

        return {}

    # =====================================================
    # BUILD REPAIR RESULT
    # =====================================================

    repair_result = RepairResult(

        field_name="summary.request_type",

        old_value=current_request_type,

        new_value=repaired_request_type,

        confidence=response.confidence,

        is_repaired=True,

        evidence=response.evidence,

        issue=issue,

        repair_agent="request_type_llm_repair"
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "repair_candidates": [

            repair_result.model_dump()
        ]
    }