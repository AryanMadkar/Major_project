import json
import re

from dotenv import load_dotenv

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

    text = state["cleaned_text"]

    amenities = []

    # ======================================
    # FAST REGEX PRECHECK
    # ======================================

    regex_map = {

        r"\bgym\b": "gym",
        r"\bgymnasium\b": "gym",
        r"\bpool\b": "swimming pool",
        r"\bswimming\b": "swimming pool",
        r"\bswiming\b": "swimming pool",
        r"\bswiming\s+pool\b": "swimming pool",
        r"\bclub\b|\bclubhouse\b": "clubhouse",
        r"\blift\b": "lift",
        r"\bparking\b": "parking",
        r"\bcctv\b": "cctv",
        r"\bsecurity\b": "security",
        r"\bgarden\b": "garden",
        r"\bplay area\b": "kids play area",
        r"\bpower backup\b": "power backup",
        r"\bmodular kitchen\b|\bmodule kitchen\b|\bmoduler kitchen\b": "modular kitchen",
        r"\bac\b|\bair conditioning\b": "air conditioning"
    }

    for pattern, value in regex_map.items():

        if re.search(pattern, text):

            amenities.append(value)

    # ======================================
    # LLM EXTRACTION
    # ======================================

    # LLM extraction: call model and parse JSON separately so failures are visible
    try:
        chain = prompt | llm
        response = chain.invoke({"message": text})
    except Exception as e:
        print("Amenities LLM invocation error:", e)
        response = None

    if response is not None:
        try:
            content = response.content.strip()

            # Remove markdown if present
            content = content.replace("```json", "")
            content = content.replace("```", "")

            parsed = json.loads(content)

            if isinstance(parsed, list):
                amenities.extend(parsed)

        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            print("Amenities parsing error:", e)

    # ======================================
    # CLEAN + DEDUP
    # ======================================

    cleaned = []

    for item in amenities:

        if not item:
            continue

        item = item.strip().lower()

        item = AMENITY_NORMALIZATION.get(item, item)

        if item in BLOCKED_GENERIC_AMENITIES:
            continue

        if item not in cleaned:

            cleaned.append(item)

    return {
        "amenities": cleaned
    }