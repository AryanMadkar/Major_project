import json
import re

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

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
# SINGLE STRUCTURED LLM CALL
# ==========================================

# We'll ask the LLM to output a single JSON object with three keys:
# - title: short professional title or null
# - contacts: array of contact person names
# - numbers: array of phone numbers (10-digit strings)

STRUCTURED_INSTRUCTION = '''
You are an expert Indian real-estate extraction assistant. Given the message below, extract the fields and return ONLY a single valid JSON object (no surrounding text, no markdown):

Fields to return:
- "title": SHORT professional title (max 12 words) or null. Prefer concise factual wording: BHK, property type, and a main location/token if available (e.g. "2BHK Flat For Rent in Andheri West"). Use "For Sale" for sale messages and "For Rent" for rent messages when request type is known. Do NOT hallucinate missing facts.
- "contacts": array of FULL PERSON NAMES. Normalize to lowercase, remove honorifics (e.g. "Mr.", "Ms.") and extra tokens, but do not split one person into first/last tokens. Return [] if none.
- "numbers": array of Indian phone numbers as 10-digit strings (no +91, no spaces/dashes). Remove duplicates. Return [] if none.

Robustness rules (important):
- Return strictly valid JSON only. If unsure, prefer empty arrays or null rather than guessing.
- Do not invent names, titles, locations, or numbers that are not present in the input.
- For partial phone numbers or ambiguous tokens, exclude them unless they clearly match an Indian 10-digit pattern.
- Keep arrays short and precise; only include items clearly present in the text.

Normalization examples:
- "Call Rahul at +91-98765 43210" → {"numbers": ["9876543210"], "contacts": ["rahul"]}
- "Looking for 1 BHK near Kanakya park, contact: Amit" → {"title": "1BHK Flat for Rent near Kanakya park", "contacts": ["amit"]}
- "No contact provided" → {"title": null, "contacts": [], "numbers": []}

Exact output example:
{"title": "2BHK Flat for Rent in Andheri West", "contacts": ["rahul"], "numbers": ["9876543210"]}
'''


def _normalize_request_label(request_type):
    if request_type == "sale":
        return "For Sale"
    if request_type == "rent":
        return "For Rent"
    return None


def _fallback_title(state: GraphState):
    bhk = state.get("bhk")
    subtype = state.get("property_subtype") or "flat"
    location = state.get("primary_location")
    request_label = _normalize_request_label(state.get("request_type"))

    if bhk is None and not location and request_label is None:
        return None

    parts = []
    if isinstance(bhk, int) and bhk > 0:
        parts.append(f"{bhk}BHK")

    parts.append(str(subtype).replace("_", " ").title())

    if request_label:
        parts.append(request_label)

    if location:
        parts.append(f"in {str(location).title()}")

    return " ".join(parts).strip() or None


def _enforce_request_type_in_title(title, request_type):
    if not title:
        return title

    request_label = _normalize_request_label(request_type)
    if request_label is None:
        return title

    if re.search(r"\bfor\s+rent\b|\bfor\s+sale\b", title, re.IGNORECASE):
        title = re.sub(r"\bfor\s+rent\b|\bfor\s+sale\b", request_label, title, flags=re.IGNORECASE)
        return title

    return f"{title} {request_label}".strip()

def safe_parse_json_object(content: str) -> dict:
    try:
        content = content.strip()
        content = content.replace("```json", "")
        content = content.replace("```", "")
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {}


# ==========================================
# REGEX NUMBER FALLBACK
# ==========================================

def regex_extract_numbers(text):

    pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}"

    matches = re.findall(pattern, text)

    cleaned = []

    for number in matches:

        number = re.sub(r"\D", "", number)

        if number.startswith("91") and len(number) > 10:
            number = number[-10:]

        if len(number) == 10:

            if number not in cleaned:

                cleaned.append(number)

    return cleaned


# ==========================================
# SAFE JSON PARSER
# ==========================================

def safe_json_array(content):

    try:

        content = content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")

        parsed = json.loads(content)

        if isinstance(parsed, list):

            return parsed

    except (json.JSONDecodeError, TypeError, AttributeError):
        pass

    return []


# ==========================================
# MAIN NODE
# ==========================================

def extract_metadata(state: GraphState):

    text = state["cleaned_text"]
    request_type = state.get("request_type")

    message_title = None

    contact_people = []

    contact_numbers = []

    # ======================================
    # SINGLE STRUCTURED LLM CALL
    # ======================================

    try:
        prompt = (
            STRUCTURED_INSTRUCTION
            + "\n\nRequest Type: "
            + str(request_type or "unknown")
            + "\n\nMessage:\n"
            + text
        )
        raw = llm.invoke(prompt)
    except Exception as e:
        print("Metadata LLM invocation error:", e)
        raw = None

    if raw is not None:
        try:
            raw_content = raw.content if hasattr(raw, "content") else str(raw)
            parsed = safe_parse_json_object(raw_content)

            if parsed.get("title") is not None:
                message_title = str(parsed.get("title")).strip() or None

            contact_people = parsed.get("contacts") or []

            contact_numbers = parsed.get("numbers") or []

        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            print("Metadata parsing error:", e)

    message_title = _enforce_request_type_in_title(message_title, request_type)

    if message_title is None:
        message_title = _fallback_title(state)

    # ======================================
    # REGEX FALLBACK FOR NUMBERS
    # ======================================

    regex_numbers = regex_extract_numbers(text)

    contact_numbers.extend(regex_numbers)

    # ======================================
    # CLEAN DEDUP
    # ======================================

    cleaned_contacts = []

    for person in contact_people:

        person = str(person).strip().lower()

        if len(person) < 2:
            continue

        if person not in cleaned_contacts:

            cleaned_contacts.append(person)

    cleaned_numbers = []

    for number in contact_numbers:

        number = re.sub(r"\D", "", str(number))

        if len(number) == 10:

            if number not in cleaned_numbers:

                cleaned_numbers.append(number)

    # ======================================
    # METADATA SUMMARY
    # ======================================

    metadata_summary = {

        "has_contact": (
            len(cleaned_numbers) > 0
            or len(cleaned_contacts) > 0
        ),

        "total_numbers": len(cleaned_numbers),

        "total_contacts": len(cleaned_contacts)
    }

    return {

        "message_title": message_title,

        "contact_people": cleaned_contacts,

        "contact_numbers": cleaned_numbers,

        "metadata_summary": metadata_summary
    }