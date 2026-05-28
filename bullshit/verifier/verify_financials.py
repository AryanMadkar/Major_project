from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, List
import json

from extractor.GraphState import GraphState


# =========================================================
# STRUCTURED OUTPUT
# =========================================================

class VerificationItem(BaseModel):

    field_name: str

    extracted_value: Optional[str] = None

    reasoning: str = Field(
        description="Detailed step-by-step verification reasoning comparing the extracted value with the original text."
    )

    is_correct: bool

    confidence: int = Field(
        ge=0,
        le=100
    )

    issue: Optional[str] = None

    evidence: Optional[str] = None


class VerificationResponse(BaseModel):

    results: List[VerificationItem]


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(
    VerificationResponse
)


# =========================================================
# PROMPTS
# =========================================================

# 1. INVESTIGATOR PROMPT (Forensic Audit Report generation)
investigator_prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """You are an elite real-estate audit investigator. Your job is to perform a rigorous forensic audit on the extracted values against the original text.

For each field, you must write a detailed, unbiased investigation report containing:
1. SUPPORTING EVIDENCE: Quote all parts of the text (with exact words) that support the extracted value. Explain why they support it.
2. CONTRADICTIONS & WEAKNESSES: Point out any contradictions, partially wrong facts, lack of explicit support, or ambiguities. (Act as a devil's advocate to find reasons why this extraction might be incorrect, misleading, or inferred without direct proof).
3. VERDICT ANALYSIS: Synthesize the findings and explain whether the extraction is 100% correct, partially correct, or incorrect.

VERIFICATION RULES BY FIELD:
1. PRICES (PRICE, RENT PRICE, DEPOSIT PRICE):
   - 'pricing.price' is the primary price. For rental requests, this should generally be the same as 'pricing.rent_price'. For sale requests, it is the purchase price.
   - 'pricing.rent_price' must match the monthly rent value.
   - 'pricing.deposit_price' must match the security deposit or advance value.
   - Pay close attention to numerical values: verify that the extracted prices don't confuse phone numbers, area values (sq ft), BHK numbers, or other price fields (e.g. rent shouldn't be mapped to deposit or vice-versa).
   - If the price is a range (e.g. "1 to 1.10 Cr") and the extraction fails to capture it or captures only one endpoint incorrectly, mark it incorrect.
   - Perform cross-field consistency checks:
     - For rental properties, the security deposit is typically greater than or equal to the monthly rent. If the deposit is extracted as less than the monthly rent, audit it extremely carefully and flag if suspicious.
     - For rental properties, if request_type is 'rent', the primary price ('pricing.price') must align with 'pricing.rent_price'.
2. PARKING COUNT:
   - Must match the exact number of parking spaces mentioned in the text.
   - If the text does not mention parking, or says "parking available" without specifying a number, then parking count should be null/None. Any non-zero count extraction in this case is incorrect.
3. PARKING TYPE:
   - Must match the specific type of parking mentioned (e.g., "open", "closed", "covered", "stilt", "basement").
   - If the type is not explicitly mentioned, it must be null/None.

Be extremely critical. Real estate errors are unacceptable."""
    ),

    (
        "human",

        """Please investigate these extracted fields:

<original_text>
{text}
</original_text>

<extracted_values>
{fields_data}
</extracted_values>

<extraction_spans>
{spans}
</extraction_spans>"""
    )
])


# 2. CHIEF JUDGE PROMPT (Structured output compile)
judge_prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """You are the Chief Real-Estate Verification Judge. Your job is to review the original text, the extracted values, the extraction spans, and the forensic audit investigation report to make the final verification verdict.

Your final output must be structured using the VerificationResponse schema.
For each field:
- Set 'field_name' to the verified field identifier exactly (use 'pricing.price', 'pricing.rent_price', 'pricing.deposit_price', 'parking.parking_count', or 'parking.parking_type').
- Set 'extracted_value' to the exact value that was extracted and provided to you for verification.
- Write a detailed step-by-step 'reasoning' summarizing the findings from the investigation and your final conclusion.
- Set 'is_correct' to true ONLY if the field is 100% correct, fully supported, and completely unambiguous. Otherwise, set it to false.
- Set 'confidence' to a score from 0 to 100 representing the certainty of your verdict.
- If incorrect, specify the exact 'issue'.
- Quote the exact 'evidence' snippet from the text if correct."""
    ),

    (
        "human",

        """Please review the evidence and issue your final judgment.

<original_text>
{text}
</original_text>

<extracted_values>
{fields_data}
</extracted_values>

<extraction_spans>
{spans}
</extraction_spans>

<forensic_investigation_report>
{investigation}
</forensic_investigation_report>"""
    )
])


# =========================================================
# NODE
# =========================================================

def verify_financials(state: GraphState):

    text = state.cleaned_text or ""

    fields_data = (
        f"pricing.price: {state.price}\n"
        f"pricing.rent_price: {state.rent_price}\n"
        f"pricing.deposit_price: {state.deposit_price}\n"
        f"parking.parking_count: {state.parking_count}\n"
        f"parking.parking_type: {state.parking_type}"
    )

    # Step 1: Run forensic investigation
    investigation_chain = investigator_prompt | llm
    investigation = investigation_chain.invoke({
        "text": text,
        "fields_data": fields_data,
        "spans": json.dumps(state.extraction_spans, indent=2)
    })

    # Step 2: Run chief judge to compile structured output
    judge_chain = judge_prompt | structured_llm
    response = judge_chain.invoke({
        "text": text,
        "fields_data": fields_data,
        "spans": json.dumps(state.extraction_spans, indent=2),
        "investigation": investigation.content
    })

    return {

        "validation_report": {

            "financial_verification":

                response.model_dump()
        }
    }
