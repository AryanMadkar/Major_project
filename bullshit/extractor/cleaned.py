import re
import emoji
import unicodedata

from .GraphState import GraphState


# =========================
# PRECOMPILED REGEX
# =========================

SPECIAL_CHAR_PATTERN = re.compile(
    r"[^a-z0-9\s₹.,]",
    re.IGNORECASE
)

MULTISPACE_PATTERN = re.compile(r"\s+")


# =========================
# TEXT CLEANER NODE
# =========================

def clean_text_node(state: GraphState):

    text = state.get("user_input", "")

    if not text:
        return {
            "cleaned_text": ""
        }

    # =====================================
    # UNICODE NORMALIZATION
    # =====================================

    text = unicodedata.normalize("NFKC", text)

    # =====================================
    # LOWERCASE
    # =====================================

    text = text.lower()

    # =====================================
    # REMOVE EMOJIS
    # =====================================

    text = emoji.replace_emoji(text, replace="")

    # =====================================
    # REMOVE SPECIAL SYMBOLS
    # =====================================

    text = SPECIAL_CHAR_PATTERN.sub(" ", text)

    # =====================================
    # REMOVE EXTRA SPACES
    # =====================================

    text = MULTISPACE_PATTERN.sub(" ", text).strip()

    return {
        "cleaned_text": text
    }