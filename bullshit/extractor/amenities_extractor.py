import json
import re

from dotenv import load_dotenv
import ahocorasick
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from .GraphState import GraphState

load_dotenv()


# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# ==========================================
# STRUCTURED OUTPUT MODEL
# ==========================================

class AmenitiesOutput(BaseModel):
    """Structured output for amenities extraction."""
    amenities: list[str]


# ==========================================
# STANDARD AMENITIES
# ==========================================

STANDARD_AMENITIES = [

    "gym",
    "swimming pool",
    "clubhouse",
    "garden",
    "kids play area",
    "parking",
    "lift",
    "security",
    "cctv",
    "power backup",
    "intercom",
    "gated community",
    "fire safety",
    "jogging track",
    "indoor games",
    "outdoor games",
    "spa",
    "sauna",
    "wifi",
    "library",
    "banquet hall",
    "community hall",
    "terrace",
    "pet friendly",
    "air conditioning",
    "modular kitchen",
    "servant room",
    "visitor parking",
    "vaastu compliant"
]


BLOCKED_GENERIC_AMENITIES = {
    "luxury amenities",
    "all amenities",
    "modern amenities",
}


AMENITY_NORMALIZATION = {
    "swimming": "swimming pool",
    "swiming": "swimming pool",
    "swiming pool": "swimming pool",
    "swimming pool": "swimming pool",
    "gymnasium": "gym",
}


# ==========================================
# AHO-CORASICK AUTOMATON (O(n) matching)
# ==========================================

def _build_automaton():
    """Build Aho-Corasick automaton for fast pattern matching."""
    A = ahocorasick.Automaton()
    
    regex_map = {
        "gym": "gym",
        "gymnasium": "gym",
        "pool": "swimming pool",
        "swimming": "swimming pool",
        "swiming": "swimming pool",
        "club": "clubhouse",
        "clubhouse": "clubhouse",
        "lift": "lift",
        "parking": "parking",
        "cctv": "cctv",
        "security": "security",
        "garden": "garden",
        "play area": "kids play area",
        "power backup": "power backup",
        "modular kitchen": "modular kitchen",
        "module kitchen": "modular kitchen",
        "moduler kitchen": "modular kitchen",
        "ac": "air conditioning",
        "air conditioning": "air conditioning",
    }
    
    for keyword, normalized in regex_map.items():
        A.add_word(keyword, normalized)
    
    A.make_automaton()
    return A

# Build automaton once at module load time
_automaton = _build_automaton()


# ==========================================
# PROMPT
# ==========================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Indian real-estate extraction AI.

Your task: Extract property amenities from the message and return ONLY a JSON array of normalized amenity names.

Guidelines:
- Output must be valid JSON array and nothing else (no markdown, no explanation).
- Prefer the provided whitelist of standard amenities. Only include non-whitelist items if they are explicit and clearly an amenity (avoid open-ended terms like "modern amenities").
- Normalize common synonyms (e.g. "pool" → "swimming pool", "ac" → "air conditioning", "modular kitchen" → "modular kitchen").
- Detect short-form/WhatsApp abbreviations ("ac", "lift", "cctv").
- Do not hallucinate amenities that are not present or only implied vaguely.

Examples:

"gym pool clubhouse"
→ ["gym", "swimming pool", "clubhouse"]

"all modern amenities"
→ []

"lift security cctv"
→ ["lift", "security", "cctv"]

"modular kitchen with ac"
→ ["modular kitchen", "air conditioning"]

Allowed standard amenities:
""" + json.dumps(STANDARD_AMENITIES)
    ),
    (
        "human",
        """
Message:

{message}
"""
    )
])


# ==========================================
# MAIN NODE
# ==========================================

def extract_amenities(state: GraphState):

    text = state.cleaned_text or ""

    if not text:
        return {"amenities": []}

    amenities = []

    # ======================================
    # FAST AHO-CORASICK MATCHING (O(n))
    # ======================================

    text_lower = text.lower()
    for end_index, normalized_amenity in _automaton.iter(text_lower):
        amenities.append(normalized_amenity)

    # ======================================
    # LLM EXTRACTION (Structured Output)
    # ======================================

    try:
        structured_llm = llm.with_structured_output(AmenitiesOutput)
        chain = prompt | structured_llm
        response = chain.invoke({"message": text})
        
        if response and hasattr(response, 'amenities'):
            amenities.extend(response.amenities)
            
    except Exception as e:
        print("Amenities LLM invocation error:", e)

    # ======================================
    # CLEAN + DEDUP
    # ======================================

    cleaned = set()

    for item in amenities:

        if not item:
            continue

        item = item.strip().lower()

        item = AMENITY_NORMALIZATION.get(item, item)

        if item in BLOCKED_GENERIC_AMENITIES:
            continue

        cleaned.add(item)

    return {
        "amenities": list(cleaned)
    }