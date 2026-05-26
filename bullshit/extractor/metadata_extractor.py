import json
import re

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# RunnableParallel may not exist in all langchain installs — provide a safe fallback.
try:
    from langchain.schema.runnable import RunnableParallel
except Exception:
    class _SimpleOut:
        def __init__(self, content):
            self.content = content

    class RunnableParallel:
        def __init__(self, **runnables):
            self._runnables = runnables

        def invoke(self, inputs: dict):
            results = {}

            for name, runnable in self._runnables.items():
                try:
                    # Try the newer Runnable API
                    res = runnable.invoke(inputs)
                except Exception:
                    try:
                        # Try common .run(text) interface
                        msg = inputs.get("message")
                        res = runnable.run(msg)
                    except Exception:
                        try:
                            # Try callable
                            res = runnable(inputs)
                        except Exception:
                            res = None

                # Normalize to object with .content attribute
                if hasattr(res, "content"):
                    results[name] = res
                else:
                    results[name] = _SimpleOut(res)

            return results

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
# TITLE CHAIN
# ==========================================

title_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Indian real-estate AI.

Generate a SHORT professional title.

Rules:
- Max 12 words
- Clean title
- Mention:
  - bhk if available
  - property type
  - location
  - rent/sale if possible
- No emojis
- No extra text

Examples:
"2BHK Flat for Rent in Andheri West"
"Office Space Available in BKC"
"Luxury Penthouse for Sale"
"""
    ),
    (
        "human",
        """
Message:

{message}
"""
    )
])

title_chain = title_prompt | llm


# ==========================================
# CONTACT PERSON CHAIN
# ==========================================

contact_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract ALL contact person names.

Rules:
- Return ONLY JSON array
- No explanations
- Ignore locations
- Ignore property names
- Ignore broker/company names unless clearly person name

Example:
["rahul", "amit shah"]
"""
    ),
    (
        "human",
        """
Message:

{message}
"""
    )
])

contact_chain = contact_prompt | llm


# ==========================================
# PHONE NUMBER CHAIN
# ==========================================

number_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract ALL phone numbers.

Rules:
- Return ONLY JSON array
- Keep only valid Indian phone numbers
- Remove spaces/dashes
- Keep duplicates removed

Example:
["9876543210", "9988776655"]
"""
    ),
    (
        "human",
        """
Message:

{message}
"""
    )
])

number_chain = number_prompt | llm


# ==========================================
# PARALLEL CHAIN
# ==========================================

parallel_chain = RunnableParallel(

    title=title_chain,

    contacts=contact_chain,

    numbers=number_chain
)


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

    except:
        pass

    return []


# ==========================================
# MAIN NODE
# ==========================================

def extract_metadata(state: GraphState):

    text = state["cleaned_text"]

    message_title = None

    contact_people = []

    contact_numbers = []

    # ======================================
    # RUN PARALLEL CHAINS
    # ======================================

    try:

        result = parallel_chain.invoke({

            "message": text
        })

        # ==================================
        # TITLE
        # ==================================

        if result.get("title"):

            message_title = result["title"].content.strip()

        # ==================================
        # CONTACTS
        # ==================================

        if result.get("contacts"):

            contact_people = safe_json_array(

                result["contacts"].content
            )

        # ==================================
        # NUMBERS
        # ==================================

        if result.get("numbers"):

            contact_numbers = safe_json_array(

                result["numbers"].content
            )

    except Exception as e:

        print("Metadata extraction error:", e)

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