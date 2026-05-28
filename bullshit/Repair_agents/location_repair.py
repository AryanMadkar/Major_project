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

class LocationRepairOutput(BaseModel):

    primary_location: Optional[str] = None

    locations: List[str] = Field(default_factory=list)

    railway_line: Optional[str] = None

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
    LocationRepairOutput
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([

    (
        "system",

        """
You are an elite Mumbai real-estate location repair agent.

Your ONLY task:
Repair incorrect location extraction.

STRICT RULES:
- Extract ONLY explicitly mentioned locations
- NEVER hallucinate locations
- NEVER invent railway lines
- Ignore amenities
- Ignore property types
- Ignore person names
- Ignore prices

PRIMARY LOCATION RULES:
- Most important locality
- Most specific locality
- Prefer actual area/locality over landmark
- Prefer final target locality

RAILWAY LINE RULES:
- western
- central
- harbour

ONLY assign railway line if strongly supported.

IMPORTANT:
- Handle spelling mistakes
- Handle shorthand
- Handle sector names
- Handle society names
- Handle station names
- Handle multiple localities

VALID EXAMPLES:
- kandivali west
- andheri east
- sector 7
- powai
- mira road
- thane west

INVALID:
- swimming pool
- 2 bhk
- fully furnished
- gym
- 9876543210

Return null if uncertain.
"""
    ),

    (
        "human",

        """
ORIGINAL TEXT:
{text}


CURRENT PRIMARY LOCATION:
{current_primary_location}


CURRENT LOCATIONS:
{current_locations}


CURRENT RAILWAY LINE:
{current_railway_line}


VERIFIER ISSUE:
{issue}


Extract corrected location details.
"""
    )
])


# =========================================================
# HELPERS
# =========================================================

def get_location_issue(validation_report):

    if not validation_report:
        return None

    section = validation_report.get(
        "contextual_verification",
        {}
    )

    results = section.get("results", [])

    failed_issues = []

    for item in results:

        if item.get("field_name") in {

            "location.primary_location",
            "location.locations",
            "location.railway_line"
        }:

            if item.get("is_correct") is False:

                issue = item.get("issue")

                if issue:
                    failed_issues.append(issue)

    if not failed_issues:
        return None

    return " | ".join(failed_issues)


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_locations(locations):

    cleaned = []

    seen = set()

    for item in locations:

        if not item:
            continue

        item = item.lower().strip()

        if item in seen:
            continue

        seen.add(item)

        cleaned.append(item)

    return cleaned


# =========================================================
# NODE
# =========================================================

def repair_location_llm(state: GraphState):

    # =====================================================
    # CHECK FAILURE
    # =====================================================

    issue = get_location_issue(
        state.validation_report
    )

    if not issue:

        return {}

    # =====================================================
    # INPUTS
    # =====================================================

    text = state.cleaned_text or ""

    current_primary_location = state.primary_location

    current_locations = state.locations or []

    current_railway_line = state.railway_line

    # =====================================================
    # INVOKE
    # =====================================================

    chain = prompt | structured_llm

    try:

        response = chain.invoke({

            "text": text,

            "current_primary_location":
                str(current_primary_location),

            "current_locations":
                ", ".join(current_locations),

            "current_railway_line":
                str(current_railway_line),

            "issue": issue
        })

    except Exception as e:

        print("Location Repair Error:", e)

        return {}

    # =====================================================
    # EMPTY
    # =====================================================

    if response is None:

        return {}

    repaired_primary_location = (
        response.primary_location
    )

    repaired_locations = (
        normalize_locations(
            response.locations
        )
    )

    repaired_railway_line = (
        response.railway_line
    )

    # =====================================================
    # NO VALID DATA
    # =====================================================

    if (
        repaired_primary_location is None
        and not repaired_locations
        and repaired_railway_line is None
    ):

        return {

            "repair_candidates": [

                RepairResult(

                    field_name="location.primary_location",

                    old_value=current_primary_location,

                    new_value=None,

                    confidence=response.confidence,

                    is_repaired=False,

                    evidence=response.evidence,

                    issue=issue,

                    repair_agent="location_llm_repair"

                ).model_dump()
            ]
        }

    # =====================================================
    # BUILD CANDIDATES
    # =====================================================

    repair_candidates = []

    # =====================================================
    # PRIMARY LOCATION
    # =====================================================

    if repaired_primary_location != current_primary_location:

        repair_candidates.append(

            RepairResult(

                field_name="location.primary_location",

                old_value=current_primary_location,

                new_value=repaired_primary_location,

                confidence=response.confidence,

                is_repaired=True,

                evidence=response.evidence,

                issue=issue,

                repair_agent="location_llm_repair"

            ).model_dump()
        )

    # =====================================================
    # LOCATIONS
    # =====================================================

    if repaired_locations != current_locations:

        repair_candidates.append(

            RepairResult(

                field_name="location.locations",

                old_value=current_locations,

                new_value=repaired_locations,

                confidence=response.confidence,

                is_repaired=True,

                evidence=response.evidence,

                issue=issue,

                repair_agent="location_llm_repair"

            ).model_dump()
        )

    # =====================================================
    # RAILWAY LINE
    # =====================================================

    if repaired_railway_line != current_railway_line:

        repair_candidates.append(

            RepairResult(

                field_name="location.railway_line",

                old_value=current_railway_line,

                new_value=repaired_railway_line,

                confidence=response.confidence,

                is_repaired=True,

                evidence=response.evidence,

                issue=issue,

                repair_agent="location_llm_repair"

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