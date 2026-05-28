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

AMENITY_ALIASES = {
    "gym": ["gym", "gymnasium", "fitness"],
    "swimming pool": ["pool", "swimming", "swiming"],
    "clubhouse": ["clubhouse", "club house", "club"],
    "garden": ["garden", "gardens", "lawn"],
    "kids play area": ["play area", "playarea", "kids play", "children play"],
    "parking": ["parking", "park", "car park"],
    "lift": ["lift", "elevator", "lifts"],
    "security": ["security", "guard", "guards"],
    "cctv": ["cctv", "camera", "cameras"],
    "power backup": ["power backup", "powerbackup", "backup", "generator", "dg"],
    "intercom": ["intercom"],
    "gated community": ["gated", "gate"],
    "fire safety": ["fire safety", "firefighting", "fire extinguisher"],
    "jogging track": ["jogging", "jogging track", "track"],
    "indoor games": ["indoor games", "indoor"],
    "outdoor games": ["outdoor games", "outdoor"],
    "spa": ["spa"],
    "sauna": ["sauna"],
    "wifi": ["wifi", "wi-fi", "internet"],
    "library": ["library"],
    "banquet hall": ["banquet", "banquet hall"],
    "community hall": ["community hall", "community centre"],
    "terrace": ["terrace", "open terrace"],
    "pet friendly": ["pet friendly", "pets allowed", "pet"],
    "air conditioning": ["ac", "a/c", "air conditioning", "airconditioner", "air conditioner"],
    "modular kitchen": ["modular kitchen", "module kitchen", "moduler kitchen"],
    "servant room": ["servant", "servants", "maid"],
    "visitor parking": ["visitor parking", "visitors parking"],
    "vaastu compliant": ["vaastu", "vastu"]
}

def validate_amenity_in_source(amenity: str, text_lower: str) -> bool:
    aliases = AMENITY_ALIASES.get(amenity, [amenity])
    for alias in aliases:
        escaped = re.escape(alias)
        # Handle word boundary:
        pattern = rf"\b{escaped}\b"
        if re.search(pattern, text_lower):
            return True
    return False

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
        A.add_word(keyword, (keyword, normalized))
    
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

Your task: Extract property amenities from the message.

Guidelines:
- Output must conform to the AmenitiesOutput structured schema.
- Prefer the provided whitelist of standard amenities. Only include non-whitelist items if they are explicit and clearly an amenity (avoid open-ended terms like "modern amenities").
- Normalize common synonyms (e.g. "pool" → "swimming pool", "ac" → "air conditioning", "modular kitchen" → "modular kitchen").
- Detect short-form/WhatsApp abbreviations ("ac", "lift", "cctv").
- STRICTLY DO NOT hallucinate or infer amenities not explicitly mentioned in the text. Never assume AC from furnishing type (furnished/semi-furnished does NOT mean AC).
- If amenity is only implied vaguely or could be a general property feature, EXCLUDE it. Only extract amenities that are EXPLICITLY NAMED.

Examples of structured outputs:

Message: "gym pool clubhouse"
Output: {{"amenities": ["gym", "swimming pool", "clubhouse"]}}

Message: "all modern amenities"
Output: {{"amenities": []}}

Message: "lift security cctv"
Output: {{"amenities": ["lift", "security", "cctv"]}}

Message: "modular kitchen with ac"
Output: {{"amenities": ["modular kitchen", "air conditioning"]}}

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
        return {
            "amenities": [],
        }

    amenities = []

    # ======================================
    # FAST AHO-CORASICK MATCHING (O(n))
    # ======================================

    text_lower = text.lower()
    for end_index, (keyword, normalized_amenity) in _automaton.iter(text_lower):
        start_index = end_index - len(keyword) + 1
        if start_index > 0 and text_lower[start_index - 1].isalnum():
            continue
        if end_index < len(text_lower) - 1 and text_lower[end_index + 1].isalnum():
            continue
        amenities.append(normalized_amenity)

    # ======================================
    # LLM EXTRACTION (Structured Output)
    # ======================================

    llm_amenities = []
    try:
        structured_llm = llm.with_structured_output(AmenitiesOutput)
        chain = prompt | structured_llm
        response = chain.invoke({"message": text})
        
        if response and hasattr(response, 'amenities'):
            llm_amenities = response.amenities
            
    except Exception as e:
        print("Amenities LLM invocation error:", e)

    # Validate LLM-extracted amenities to prevent hallucination
    validated_llm_amenities = []
    for item in llm_amenities:
        if not item:
            continue
        item_lower = item.strip().lower()
        item_normalized = AMENITY_NORMALIZATION.get(item_lower, item_lower)
        if validate_amenity_in_source(item_normalized, text_lower):
            validated_llm_amenities.append(item_normalized)
        else:
            print(f"Rejected hallucinated amenity: {item_normalized}")

    amenities.extend(validated_llm_amenities)

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

    # ======================================
    # RECORD SPANS
    # ======================================
    extraction_spans = {}
    amenities_spans = []
    for item in cleaned:
        m = re.search(rf"\b{re.escape(item)}\b", text_lower)
        if not m:
            m = re.search(re.escape(item), text_lower)
        if m:
            amenities_spans.append({
                "value": item,
                "source_span": text[m.start():m.end()],
                "start": m.start(),
                "end": m.end(),
                "extractor": "amenities_automaton_or_llm"
            })
    if amenities_spans:
        extraction_spans["amenities"] = {
            "value": list(cleaned),
            "source_span": ", ".join(s["source_span"] for s in amenities_spans),
            "start": min(s["start"] for s in amenities_spans),
            "end": max(s["end"] for s in amenities_spans),
            "extractor": "amenities_automaton_or_llm"
        }

    return {
        "amenities": list(cleaned),
        "extraction_spans": extraction_spans
    }