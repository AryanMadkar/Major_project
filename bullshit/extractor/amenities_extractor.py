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


# ==========================================
# PROMPT
# ==========================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Indian real-estate extraction AI.

Your task:

Extract ALL property amenities from the message.

Rules:
- Return ONLY valid JSON
- Output must be an array
- Detect implicit amenities
- Understand WhatsApp abbreviations
- Normalize names
- Ignore non-amenity words

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
        r"\bpool\b": "swimming pool",
        r"\bclub\b|\bclubhouse\b": "clubhouse",
        r"\blift\b": "lift",
        r"\bparking\b": "parking",
        r"\bcctv\b": "cctv",
        r"\bsecurity\b": "security",
        r"\bgarden\b": "garden",
        r"\bplay area\b": "kids play area",
        r"\bpower backup\b": "power backup",
        r"\bmodular kitchen\b": "modular kitchen",
        r"\bac\b|\bair conditioning\b": "air conditioning"
    }

    for pattern, value in regex_map.items():

        if re.search(pattern, text):

            amenities.append(value)

    # ======================================
    # LLM EXTRACTION
    # ======================================

    try:

        chain = prompt | llm

        response = chain.invoke({
            "message": text
        })

        content = response.content.strip()

        # Remove markdown if present
        content = content.replace("```json", "")
        content = content.replace("```", "")

        parsed = json.loads(content)

        if isinstance(parsed, list):

            amenities.extend(parsed)

    except Exception as e:

        print("Amenities extraction error:", e)

    # ======================================
    # CLEAN + DEDUP
    # ======================================

    cleaned = []

    for item in amenities:

        if not item:
            continue

        item = item.strip().lower()

        if item not in cleaned:

            cleaned.append(item)

    return {
        "amenities": cleaned
    }