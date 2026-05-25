# -*- coding: utf-8 -*-
import os
import re
import glob
import random
import logging
import unicodedata
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()
logging.basicConfig(level=logging.INFO)


# =========================================================
# OUTPUT SCHEMA
# =========================================================

class SegmentedMessages(BaseModel):
    messages: List[str] = Field(
        description="Independent property listing messages"
    )


# =========================================================
# LLM
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not found in environment; LLM calls will be skipped.")
    llm = None
    structured_llm = None
else:
    # set the key in the environment for the client library to consume
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    structured_llm = llm.with_structured_output(SegmentedMessages)


# =========================================================
# CLEANER
# =========================================================

def clean_text(text: str) -> str:
    # remove emojis/symbols (wide unicode ranges)
    emoji_re = re.compile(
        "[\U0001F300-\U0001F6FF\U0001F900-\U0001F9FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]+",
        flags=re.UNICODE,
    )

    text = emoji_re.sub("", text)

    # normalize unicode (decompose accents)
    text = unicodedata.normalize("NFKC", text)

    # normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    # normalize line breaks
    text = re.sub(r"\n{3,}", "\n\n", text)

    # strip leading/trailing whitespace per line
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join([ln for ln in lines if ln]).strip()


def normalize_to_single_line(text: str) -> str:
    """Convert a multiline property chunk into a compact single-line string."""
    parts = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return " ; ".join(parts)


# =========================================================
# PROPERTY START DETECTOR
# =========================================================

PROPERTY_START_PATTERNS = [
    r"^\d+(?:\.\d+)?\s*bhk\b",
    r"^\d+\s*rk\b",
    r"^\d+\s*bed\b",
    r"^\d+\s*beds?\b",
    r"^(flat|apartment|office|shop|villa|plot)\b",
    r"^(available inventory|urgent sale|for sell|for sale)\b",
    r"^[•\u25CF\u2022🔹🏢🏠🏡]\s*",
    r"^[A-Z][A-Za-z0-9\s\-&,]{3,}$",
]


def looks_like_property_start(line: str) -> bool:

    line = line.strip().lower()

    for pattern in PROPERTY_START_PATTERNS:
        if re.search(pattern, line):
            return True

    return False


# =========================================================
# HEURISTIC PRE-SPLITTER
# =========================================================

def heuristic_split(text: str) -> List[str]:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    chunks = []
    current_chunk = []

    for line in lines:

        # start new property
        if looks_like_property_start(line):

            if current_chunk:
                chunks.append("\n".join(current_chunk))

            current_chunk = [line]

        else:
            current_chunk.append(line)

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks


def split_into_blocks(text: str) -> List[str]:
    """Split raw text into higher-level blocks using blank lines and bullet/group markers.

    This helps avoid over-segmentation line-by-line and preserves logical groups.
    """
    # split on two-or-more newlines first
    parts = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    blocks = []
    for p in parts:
        # further split long blocks that contain bullet separators
        if re.search(r"^\s*[•\u2022\u25CF\-\*]\s+", p, flags=re.M):
            # split by lines starting with bullets
            lines = [ln.strip() for ln in p.splitlines() if ln.strip()]
            current = []
            for ln in lines:
                if re.match(r"^[•\u2022\u25CF\-\*\s]*[•\u2022\u25CF\-\*]\s+", ln):
                    if current:
                        blocks.append("\n".join(current))
                    current = [ln]
                else:
                    current.append(ln)
            if current:
                blocks.append("\n".join(current))
        else:
            blocks.append(p)

    return blocks


# ------------------
# Price / Area parsing
# ------------------

PRICE_RE = re.compile(r"(₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)(\s*(cr|crore|lakh|lac|k|thousand|m|million))?", flags=re.I)
AREA_RE = re.compile(r"([\d,.]+)\s*(sqft|sq\.ft|sq ft|sqm|sq\.m|m2|sqmt|sq\.mtr|sq\.meter|sq meter|sq feet)\b", flags=re.I)


def parse_price(text: str) -> Tuple[float, str]:
    """Extract numeric price in INR and return (amount, unit_str).

    Returns amount as a float in INR (e.g., 37800000.0) when parseable, else (0.0, "").
    Supports crore/lakh/k/million suffixes.
    """
    m = PRICE_RE.search(text.replace(",", ""))
    if not m:
        return (0.0, "")

    num = float(m.group(2))
    suf = (m.group(4) or "").lower() if m.group(4) else ""

    if suf in ("cr", "crore"):
        num = num * 1e7
    elif suf in ("lakh", "lac"):
        num = num * 1e5
    elif suf in ("k", "thousand"):
        num = num * 1e3
    elif suf in ("m", "million"):
        num = num * 1e6

    return (num, "INR")


def parse_area(text: str) -> Tuple[float, str]:
    """Extract area and normalize to sqft where possible. Returns (value, unit).

    If unit is metric (sqm/m2), convert to sqft (~10.7639).
    """
    m = AREA_RE.search(text.replace(",", ""))
    if not m:
        return (0.0, "")

    val = float(m.group(1))
    unit = m.group(2).lower()

    if unit in ("sqm", "sq.m", "m2", "sqmt", "sq.mtr", "sq meter", "sq\.meter"):
        val = val * 10.7639
        unit = "sqft"
    else:
        # normalize common sqft spellings
        unit = "sqft"

    return (val, unit)


def deduplicate_semantic_parts(text: str) -> str:
    """Remove duplicate semantic fragments while preserving order.

    Splits on common separators and filters exact / case-insensitive duplicates.
    Returns a reconstructed single-line string.
    """
    # split on common separators
    parts = re.split(r"[;|\n\\/,-]{1,}\s*", text)
    seen = set()
    out = []
    for p in parts:
        p_clean = p.strip()
        if not p_clean:
            continue
        key = re.sub(r"\s+", " ", p_clean).lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(p_clean)

    return " ; ".join(out)


def detect_global_header_footer(text: str) -> Tuple[List[str], List[str]]:
    """Return (header_lines, footer_lines) that appear before the first property and after the last property.

    Header/footer are raw lines found outside detected property starts.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    start_idxs = [i for i, ln in enumerate(lines) if looks_like_property_start(ln)]

    if not start_idxs:
        return ([], [])

    first = start_idxs[0]
    last = start_idxs[-1]

    header = lines[:first]
    footer = lines[last + 1 :]

    # refine header/footer: drop lines that look like property details (price/area/bhk)
    def filter_meta(lines_list):
        out = []
        for ln in lines_list:
            if PRICE_RE.search(ln) or AREA_RE.search(ln) or looks_like_property_start(ln):
                # treat as part of body, not header/footer
                continue
            # keep short informative lines
            if len(ln) > 200:
                continue
            out.append(ln)
        return out

    header = filter_meta(header)
    footer = filter_meta(footer)

    # only treat as header/footer if not too long
    if len(header) > 8:
        header = header[:8]
    if len(footer) > 8:
        footer = footer[-8:]

    return (header, footer)


def build_examples_from_dataset(dataset_dir: str, max_examples: int = 3) -> List[Tuple[str, List[str]]]:
    """Scan `dataset_dir` for md files and produce (raw, [single-line outputs]) examples.

    These are pseudo-ground-truth examples created using the heuristic splitter and normalizer.
    """
    examples = []
    paths = glob.glob(os.path.join(dataset_dir, "**", "*.md"), recursive=True)
    random.shuffle(paths)

    scored = []
    for p in paths:
        try:
            text = Path(p).read_text(encoding="utf-8")
        except Exception:
            continue

        cleaned = clean_text(text)
        chunks = heuristic_split(cleaned)
        if not chunks:
            continue

        # score quality: prefer examples containing price & area & multiple chunks
        score = 0
        joined = "\n\n".join(chunks[:3])
        for ln in chunks[:5]:
            if PRICE_RE.search(ln):
                score += 3
            if AREA_RE.search(ln):
                score += 2
            if looks_like_property_start(ln):
                score += 1

        outputs = [normalize_to_single_line(c) for c in chunks[:5]]
        raw_sample = "\n\n".join(chunks[:3])
        scored.append((score, raw_sample, outputs))

    # pick top-scoring examples
    scored.sort(key=lambda x: x[0], reverse=True)
    for sc, raw_sample, outputs in scored[:max_examples]:
        examples.append((raw_sample, outputs))

    return examples


# =========================================================
# ZERO-SHOT PROMPT
# =========================================================

def build_prompt_with_examples(examples: List[Tuple[str, List[str]]], chunks_text: str, header: List[str], footer: List[str], prompt_variant: int = 0):
    # prompt_variant selects between different system wordings/tone for robustness
    if prompt_variant == 0:
        system_message = """
You are an expert AI for semantic segmentation of real-estate WhatsApp messages.

Your task:
Convert noisy candidate chunks into PERFECT independent property messages.

STRICT RULES:
- One property per message
- Merge multiline details correctly
- Preserve all useful details
- Remove decorative/marketing noise
- Do not hallucinate
- Do not invent fields
- Do not summarize
- Keep original wording as much as possible

NEVER infer missing information. NEVER copy details from neighboring properties. If uncertain, preserve raw text exactly.
Return ONLY structured output: a JSON object with key `messages` containing an array of property strings.
"""
    else:
        system_message = """
You are a meticulous extractor for property listings shared in noisy chat messages.

Goal:
Produce a clean list of independent property descriptions suitable for database ingestion.

RULES (strict):
- Output one property per element
- Preserve numeric details (area, price, BHK) verbatim where possible
- Attach global header/footer info to each property when relevant
- Remove marketing emojis and filler
- Do not invent new facts

NEVER infer missing information. NEVER copy details from neighboring properties. If uncertain, preserve raw text exactly.
Return ONLY structured JSON with key `messages` containing an array of property strings.
"""

    human_template = """
Header (applies to all properties):
{header}

Footer (applies to all properties):
{footer}

Examples:
{examples_section}

Candidate property chunks:

{chunks}
"""

    # build examples section
    ex_lines = []
    for raw, outputs in examples:
        ex_lines.append("RAW:\n" + raw)
        ex_lines.append("OUTPUT:\n" + "\n".join(outputs))
        ex_lines.append("---")

    examples_section = "\n".join(ex_lines)

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_template),
    ])

    formatted = {
        "header": "\n".join(header) if header else "",
        "footer": "\n".join(footer) if footer else "",
        "examples_section": examples_section,
        "chunks": chunks_text,
    }

    return prompt, formatted


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert AI for semantic segmentation of real-estate WhatsApp messages.

Your task:
Convert noisy candidate chunks into PERFECT independent property messages.

STRICT RULES:
- One property per message
- Merge multiline details correctly
- Preserve all useful details
- Remove decorative/marketing noise
- Do not hallucinate
- Do not invent fields
- Do not summarize
- Keep original wording as much as possible

Return ONLY structured output.
"""
    ),
    (
        "human",
        """
Candidate property chunks:

{chunks}
"""
    )
])


# =========================================================
# CHAIN
# =========================================================

if structured_llm is not None:
    try:
        chain = prompt | structured_llm
    except Exception:
        logging.exception("Failed to compose prompt and LLM chain. LLM calls will be skipped.")
        chain = None
else:
    chain = None


# =========================================================
# MAIN FUNCTION
# =========================================================

def split_property_messages_improved(text: str, use_llm: bool = True, max_examples: int = 3) -> List[str]:
    """Improved splitter that handles global header/footer, few-shot prompting, and LLM fallback.

    Returns a list of single-line property strings.
    """
    cleaned = clean_text(text)

    # detect header/footer
    header, footer = detect_global_header_footer(cleaned)

    # remove header/footer from the body for clearer chunking
    body_lines = [ln for ln in cleaned.splitlines() if ln.strip()]
    if header:
        body_lines = body_lines[len(header):]
    if footer:
        body_lines = body_lines[: -len(footer)] if footer else body_lines

    body_text = "\n".join(body_lines)

    # first split into blocks, then into properties inside blocks
    blocks = split_into_blocks(body_text)
    heuristic_chunks = []
    for block in blocks:
        # inside each block, run line-based heuristic split
        sub_chunks = heuristic_split(block)
        # if heuristic split returns a single large chunk, try splitting by punctuation/blank lines
        if len(sub_chunks) == 1 and (len(block) > 800 or block.count('\n') > 6):
            # attempt a fallback split by double newlines inside the block
            for part in re.split(r"\n{2,}", block):
                if part.strip():
                    heuristic_chunks.extend(heuristic_split(part))
        else:
            heuristic_chunks.extend(sub_chunks)

    # apply header/footer selectively
    def should_propagate_header(header_lines: List[str]) -> bool:
        # only propagate very short headers (project/tower names)
        if not header_lines:
            return False
        if len(header_lines) > 2:
            return False
        # heuristic: header looks like project name if short and title-cased
        for hl in header_lines:
            if len(hl.split()) <= 6 and re.match(r"^[A-Z0-9][A-Za-z0-9\s\-&,]+$", hl):
                return True
        return False

    propagate_header = should_propagate_header(header)

    def apply_context(chunk: str) -> str:
        parts = []
        if propagate_header:
            parts.extend(header)
        parts.append(chunk)
        # do not propagate footer unless it's exceptionally short
        if footer and len(footer) <= 2:
            parts.extend(footer)
        return "\n".join(parts)

    # build examples from dataset
    dataset_dir = os.path.join(os.path.dirname(__file__), "..", "multi_property_dataset")
    dataset_dir = os.path.normpath(dataset_dir)
    examples = []
    if os.path.isdir(dataset_dir):
        examples = build_examples_from_dataset(dataset_dir, max_examples=max_examples)

    # if LLM not configured or disabled, return normalized heuristic outputs
    if not use_llm or chain is None:
        logging.info("Returning heuristic normalized outputs (LLM disabled/unavailable).")
        return [normalize_to_single_line(apply_context(c)) for c in heuristic_chunks]

    # choose prompt variant: prefer variant 1 if we have good examples, else 0
    prompt_variant = 0
    if len(examples) >= 2:
        prompt_variant = 1
    else:
        prompt_variant = 0 if random.random() < 0.8 else 1

    final_messages = []

    # Process each property separately to avoid cross-contamination
    for chunk in heuristic_chunks:
        chunk_text = apply_context(chunk)

        prompt_obj, formatted = build_prompt_with_examples(examples, chunk_text, header if propagate_header else [], footer if (footer and len(footer) <= 2) else [], prompt_variant=prompt_variant)

        try:
            dynamic_chain = prompt_obj | structured_llm
        except Exception:
            logging.exception("Failed to compose dynamic chain for chunk; using heuristic chunk.")
            final_messages.append(normalize_to_single_line(chunk_text))
            continue

        try:
            response = dynamic_chain.invoke(formatted)
        except Exception:
            logging.exception("LLM invocation failed for chunk; falling back to heuristic chunk.")
            final_messages.append(normalize_to_single_line(chunk_text))
            continue

        # extract messages from structured output
        msgs = []
        if hasattr(response, "messages"):
            for m in response.messages:
                m = re.sub(r"\s+", " ", m).strip()
                if m:
                    msgs.append(m)
        else:
            # best-effort parse
            text_out = str(response)
            for ln in text_out.splitlines():
                ln = ln.strip()
                if ln:
                    msgs.append(ln)

        # validation: ensure at most one primary price and one area per listing
        def validate_listing_text(s: str) -> bool:
            prices = PRICE_RE.findall(s)
            areas = AREA_RE.findall(s)
            # basic checks
            if len(prices) > 1 or len(areas) > 1:
                return False
            return True

        for m in msgs:
            if not validate_listing_text(m):
                logging.warning("Listing failed validation; using heuristic fallback for chunk.")
                final_messages.append(normalize_to_single_line(chunk_text))
            else:
                # dedupe semantic fragments before finalizing
                final_messages.append(normalize_to_single_line(deduplicate_semantic_parts(m)))

    return final_messages


# Backwards-compatible wrapper
def split_property_messages(text: str, use_llm: bool = True, max_examples: int = 3) -> List[str]:
    """Compatibility wrapper kept for callers that expect `split_property_messages`.

    Delegates to `split_property_messages_improved`.
    """
    return split_property_messages_improved(text, use_llm=use_llm, max_examples=max_examples)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    FOR SELL READY TO MOVE

    3 BHK
    1036 Sqft
    Sunteck City
    3.78 Cr

    3 BHK
    Ekta Tripolis
    Goregaon West
    4.10 Cr

    2 BHK
    Rustomjee Elanza
    2.90 Cr
    """

    result = split_property_messages(sample)

    print("\nRESULT:\n")

    for i, msg in enumerate(result, start=1):
        print(f"{i}. {msg}")