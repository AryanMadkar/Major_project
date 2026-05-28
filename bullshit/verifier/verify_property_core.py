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
1. BHK:
   - Must match the exact number of bedrooms mentioned. E.g., "1 BHK" -> 1.
   - If the text specifies "1.5 BHK" but the extraction says "1", it is incorrect (partially wrong).
   - If the text has a range (e.g., "1/2 BHK") and the extraction doesn't match the specific requirement, mark it incorrect.
2. PROPERTY SUBTYPE:
   - Must match the specific residential or commercial subtype mentioned (e.g., flat, apartment, shop, office, villa, penthouse, row house).
   - Broad categories (like "apartment" instead of "flat") are correct if semantically identical in context, but completely different types (e.g., "villa" when text says "flat") are incorrect.
3. REQUEST TYPE:
   - Must correctly verify the intent: "requirement" (buyer looking to purchase, tenant looking to rent) vs. "availability" (owner/agent selling, renting out).
   - Keywords like "wanted", "required", "looking for" -> requirement/buy/rent.
   - Keywords like "available", "to let", "for sale", "outrate" -> availability/sell/rent_out.

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
- Set 'field_name' to the verified field identifier exactly (use 'summary.bhk', 'property.property_subtype', or 'summary.request_type').
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

def verify_property_core(state: GraphState):

    text = state.cleaned_text or ""

    fields_data = (
        f"summary.bhk: {state.bhk}\n"
        f"property.property_subtype: {state.property_subtype}\n"
        f"summary.request_type: {state.request_type}"
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

            "property_core_verification":

                response.model_dump()
        }
    }
