import json
import re
from functools import lru_cache

from cachetools import TTLCache
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from .GraphState import GraphState

load_dotenv()

# =========================================================
# REGEX COMPILE
# =========================================================

PHONE_PATTERN = re.compile(
    r"(?:\+91[\-\s]?)?[6-9]\d{9}"
)

MULTISPACE_PATTERN = re.compile(r"\s+")

# =========================================================
# CACHE
# =========================================================

metadata_cache = TTLCache(
    maxsize=10000,
    ttl=3600
)

# =========================================================
# STRUCTURED OUTPUT MODEL
# =========================================================

class MetadataResponse(BaseModel):

    contacts: list[str] = Field(default_factory=list)

    numbers: list[str] = Field(default_factory=list)


# =========================================================
# LLM SINGLETON
# =========================================================

@lru_cache
def get_llm():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    return llm.with_structured_output(MetadataResponse)


# =========================================================
# PROMPT
# =========================================================

CONTACT_PROMPT = """
You are an expert Indian real-estate extraction assistant.

Extract ONLY:

1. contact person names
2. Indian phone numbers

Rules:
- Return only clearly visible information
- Do not hallucinate
- Normalize names to lowercase
- Remove duplicate numbers
- Phone numbers must be valid Indian 10 digit numbers
"""

# =========================================================
# HELPERS
# =========================================================

def normalize_text(text: str):

    text = MULTISPACE_PATTERN.sub(" ", text)

    return text.strip()


def regex_extract_numbers(text: str):

    matches = PHONE_PATTERN.findall(text)

    cleaned = set()

    for number in matches:

        number = re.sub(r"\D", "", number)

        if number.startswith("91") and len(number) > 10:
            number = number[-10:]

        if len(number) == 10:
            cleaned.add(number)

    return list(cleaned)


def build_title(state: GraphState):

    bhk = state.bhk

    subtype = state.property_subtype or "Flat"

    location = state.primary_location

    request_type = state.request_type

    parts = []

    if isinstance(bhk, int):
        parts.append(f"{bhk}BHK")

    parts.append(str(subtype).title())

    if request_type == "rent":
        parts.append("For Rent")

    elif request_type == "sale":
        parts.append("For Sale")

    if location:
        parts.append(f"in {location.title()}")

    title = " ".join(parts).strip()

    return title if title else None


def clean_contacts(contacts):

    cleaned = []

    for person in contacts:

        person = str(person).strip().lower()

        if len(person) < 2:
            continue

        if person not in cleaned:
            cleaned.append(person)

    return cleaned


def clean_numbers(numbers):

    cleaned = set()

    for number in numbers:

        number = re.sub(r"\D", "", str(number))

        if number.startswith("91") and len(number) > 10:
            number = number[-10:]

        if len(number) == 10:
            cleaned.add(number)

    return list(cleaned)


# =========================================================
# SPAN TRACING HELPER
# =========================================================

def record_metadata_spans(state, text, message_title, contact_people, contact_numbers) -> dict:
    extraction_spans = {}
    
    number_spans = []
    for num in contact_numbers or []:
        m = re.search(re.escape(str(num)), text)
        if m:
            number_spans.append({
                "value": num,
                "source_span": m.group(0),
                "start": m.start(),
                "end": m.end()
            })
    if number_spans:
        extraction_spans["metadata.contact_numbers"] = {
            "value": contact_numbers,
            "source_span": ", ".join(s["source_span"] for s in number_spans),
            "start": min(s["start"] for s in number_spans),
            "end": max(s["end"] for s in number_spans),
            "extractor": "phone_regex_or_llm"
        }
        
    people_spans = []
    for person in contact_people or []:
        m = re.search(rf"\b{re.escape(str(person))}\b", text.lower())
        if m:
            people_spans.append({
                "value": person,
                "source_span": m.group(0),
                "start": m.start(),
                "end": m.end()
            })
    if people_spans:
        extraction_spans["metadata.contact_people"] = {
            "value": contact_people,
            "source_span": ", ".join(s["source_span"] for s in people_spans),
            "start": min(s["start"] for s in people_spans),
            "end": max(s["end"] for s in people_spans),
            "extractor": "contact_name_llm"
        }
        
    if message_title:
        comp_starts = []
        comp_ends = []
        prev_spans = state.extraction_spans or {}
        for key in ["summary.bhk", "property.property_subtype", "location.primary_location"]:
            if key in prev_spans:
                comp_starts.append(prev_spans[key]["start"])
                comp_ends.append(prev_spans[key]["end"])
        if comp_starts and comp_ends:
            start = min(comp_starts)
            end = max(comp_ends)
            extraction_spans["metadata.message_title"] = {
                "value": message_title,
                "source_span": text[start:end],
                "start": start,
                "end": end,
                "extractor": "title_rule_generator"
            }
        else:
            extraction_spans["metadata.message_title"] = {
                "value": message_title,
                "source_span": text[:30],
                "start": 0,
                "end": min(30, len(text)),
                "extractor": "title_rule_generator"
            }
            
    return extraction_spans


# =========================================================
# MAIN NODE
# =========================================================

def extract_metadata(state: GraphState):



    text = state.cleaned_text or ""

    if not text:
        return {
            "extraction_spans": {}
        }

    text = normalize_text(text)

    # =====================================================
    # CACHE CHECK
    # =====================================================

    cache_key = hash(text)

    if cache_key in metadata_cache:

        cached = metadata_cache[cache_key]

        message_title = cached["message_title"]

        contact_people = cached["contact_people"]

        contact_numbers = cached["contact_numbers"]

        metadata_summary = cached["metadata_summary"]

        extraction_spans = record_metadata_spans(state, text, message_title, contact_people, contact_numbers)
        return {
            "message_title": message_title,
            "contact_people": contact_people,
            "contact_numbers": contact_numbers,
            "metadata_summary": metadata_summary,
            "extraction_spans": extraction_spans
        }

    # =====================================================
    # REGEX FIRST
    # =====================================================

    regex_numbers = regex_extract_numbers(text)

    contact_people = []

    contact_numbers = regex_numbers.copy()

    # =====================================================
    # CALL LLM FOR NAMES (Always call LLM to ensure names are extracted)
    # =====================================================

    try:

        llm = get_llm()

        response = llm.invoke(
            CONTACT_PROMPT + "\n\nMESSAGE:\n" + text
        )

        if response:

            contact_people = response.contacts or []

            # Also extend numbers found by LLM (some tricky formatting regex might miss)
            contact_numbers.extend(
                response.numbers or []
            )

    except Exception as e:

        print("Metadata LLM Error:", e)

    # =====================================================
    # CLEANING
    # =====================================================

    contact_people = clean_contacts(contact_people)

    contact_numbers = clean_numbers(contact_numbers)

    # =====================================================
    # TITLE GENERATION
    # =====================================================

    message_title = build_title(state)

    # =====================================================
    # SUMMARY
    # =====================================================

    metadata_summary = {

        "has_contact": (
            len(contact_people) > 0
            or len(contact_numbers) > 0
        ),

        "total_contacts": len(contact_people),

        "total_numbers": len(contact_numbers)
    }

    extraction_spans = record_metadata_spans(state, text, message_title, contact_people, contact_numbers)

    return {
        "message_title": message_title,
        "contact_people": contact_people,
        "contact_numbers": contact_numbers,
        "metadata_summary": metadata_summary,
        "extraction_spans": extraction_spans
    }