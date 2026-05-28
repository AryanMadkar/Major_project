from typing import Optional, List, Dict

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

class PriceRepairOutput(BaseModel):

    price: Optional[int] = Field(None, description="Corrected primary price (purchase price for sale, or monthly rent for rent requests)")
    rent_price: Optional[int] = Field(None, description="Corrected monthly rent price")
    deposit_price: Optional[int] = Field(None, description="Corrected security deposit / advance price")

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
    PriceRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite real-estate price repair agent.

Your ONLY task:
Repair incorrect property price extractions (pricing.price, pricing.rent_price, pricing.deposit_price).

STRICT RULES:
- Extract ONLY explicit property prices (sale price, rent price, deposit price)
- NEVER infer
- Ignore phone numbers
- Ignore parking counts
- Ignore BHK numbers
- Ignore sqft/area measurements
- Ignore timestamps

IMPORTANT:
- Convert lakh/lac/lacs to full integer (e.g. 45k -> 45000, 1.25 lakh -> 125000, 1.5 lakh -> 150000)
- Convert crore/cr to full integer
- Return integer only or null if not mentioned.
- For rental requests: 'pricing.price' (primary price) must match 'pricing.rent_price' (monthly rent).

Examples:
1 lakh → 100000
95 lakh → 9500000
1.2 cr → 12000000

IGNORE:
- 9876543210
- 2 bhk
- 850 sqft
- 2 parking

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}

CURRENT EXTRACTED VALUES:
Price: {current_price}
Rent Price: {current_rent_price}
Deposit Price: {current_deposit_price}

REQUEST TYPE:
{request_type}

VERIFIER ISSUES:
{issues}

Extract corrected property prices.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_price_issues(validation_report) -> Dict[str, str]:
    issues = {}
    if not validation_report:
        return issues

    section = validation_report.get(
        "financial_verification",
        {}
    )

    results = section.get("results", [])

    for item in results:
        field = item.get("field_name")
        if field in {"pricing.price", "pricing.rent_price", "pricing.deposit_price"}:
            if item.get("is_correct") is False:
                issues[field] = item.get("issue") or "Incorrect value"

    return issues


# =========================================================
# NODE
# =========================================================

def repair_price_llm(state: GraphState):

    # =====================================================
    # CHECK IF ANY PRICE FIELDS FAILED
    # =====================================================

    issues = get_price_issues(
        state.validation_report
    )

    if not issues:
        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""
    current_price = state.price
    current_rent_price = state.rent_price
    current_deposit_price = state.deposit_price
    request_type = state.request_type or "unknown"

    issues_str = "\n".join(f"- {field}: {issue}" for field, issue in issues.items())

    # =====================================================
    # INVOKE LLM
    # =====================================================

    chain = prompt | structured_llm

    try:
        response = chain.invoke({
            "text": text,
            "current_price": str(current_price),
            "current_rent_price": str(current_rent_price),
            "current_deposit_price": str(current_deposit_price),
            "request_type": request_type,
            "issues": issues_str
        })
    except Exception as e:
        print("Price Repair Error:", e)
        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:
        return {}

    # =====================================================
    # BUILD REPAIR CANDIDATES
    # =====================================================

    repair_candidates = []

    # Map target fields to their extracted value and response value
    field_mappings = [
        ("pricing.price", current_price, response.price),
        ("pricing.rent_price", current_rent_price, response.rent_price),
        ("pricing.deposit_price", current_deposit_price, response.deposit_price),
    ]

    for field_name, current_val, repaired_val in field_mappings:
        # Only issue repair candidates for fields that actually had verification issues
        if field_name in issues:
            issue = issues[field_name]
            
            if repaired_val != current_val:
                repair_result = RepairResult(
                    field_name=field_name,
                    old_value=current_val,
                    new_value=repaired_val,
                    confidence=response.confidence,
                    is_repaired=True,
                    evidence=response.evidence,
                    issue=issue,
                    repair_agent="price_llm_repair"
                )
                repair_candidates.append(repair_result.model_dump())

    if not repair_candidates:
        return {}

    return {
        "repair_candidates": repair_candidates
    }