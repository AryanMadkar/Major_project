import re
import unicodedata
from typing import TypedDict, Optional
from .GraphState import GraphState

# =========================
# TEXT CLEANER NODE
# =========================
def clean_text_node(state: GraphState):

    text = state["user_input"]

    # =====================================
    # LOWERCASE
    # =====================================
    text = text.lower()

    # =====================================
    # REMOVE EMOJIS
    # =====================================
    text = remove_emojis(text)

    # =====================================
    # REMOVE SPECIAL SYMBOLS
    # keeps alphabets + numbers + spaces
    # =====================================
    text = re.sub(r"[^a-z0-9\s₹.,]", " ", text)
    # =====================================
    # REMOVE EXTRA SPACES
    # =====================================
    text = re.sub(r"\s+", " ", text).strip()

    return {
        "cleaned_text": text
    }


# =========================
# EMOJI REMOVER
# =========================
def remove_emojis(text):

    cleaned = []

    for char in text:

        # Skip emoji unicode ranges
        if unicodedata.category(char) == "So":
            continue

        cleaned.append(char)

    return "".join(cleaned)