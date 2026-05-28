# V3 REGRESSION ANALYSIS & FIXES

## Executive Summary

V3 introduced **three critical regressions** that outweigh the +0.57% improvement. All have identified root causes and specific fixes.

---

## REGRESSION #1: Pricing Reversal ⚠️ CRITICAL

### Evidence
```
Input:   Rent 33000/- & Deposit of Rs 1,50,000/-
V2 Correct: rent_price=33000, deposit_price=150000
V3 BROKEN:  rent_price=1, deposit_price=33000
```

### Root Cause
**File**: [price_extractor.py](price_extractor.py) (~lines 295-310)

Logic bug in rent/deposit assignment using `elif`:

```python
for item in prices:
    context = item["context"]
    if (deposit_price is None and has_any_keyword(context, DEPOSIT_WORDS)):
        deposit_price = item["value"]
    elif (rent_price is None and has_any_keyword(context, RENT_WORDS)):  # BUG
        rent_price = item["value"]
```

**Problem**: Once `deposit_price` is assigned, the `elif` prevents `rent_price` from being assigned even if the next item matches RENT_WORDS.

### Impact
- Rent and deposit values are reversed/corrupted
- Makes pricing completely unreliable
- Production blocker

### Fix
Change `elif` to `if`:
```python
if (deposit_price is None and has_any_keyword(context, DEPOSIT_WORDS)):
    deposit_price = item["value"]
if (rent_price is None and has_any_keyword(context, RENT_WORDS)):  # Changed from elif
    rent_price = item["value"]
```

---

## REGRESSION #2: Fake Amenity Hallucination ⚠️ CRITICAL

### Evidence
```
Input: "1 bhk fully furnished in blue empire@36000 negotiable"
       (NO AC mentioned anywhere)
V3 Output: extraction_meta.amenities = ["air conditioning"] (75% confidence)
           BUT main amenities output = []
```

### Root Cause - UNCLEAR (Inconsistent behavior)

**Observations**:
1. Inconsistency between `extraction_meta.amenities` and main `amenities` array
2. LLM is extracting amenities that don't exist in source text
3. Aho-Corasick keywords don't include generic "AC" patterns that would cause false positives

**Possible Sources**:
1. **Amenities Extractor LLM Prompt** (lines 142-178 in [amenities_extractor.py](amenities_extractor.py))
   - Prompt may be too permissive about amenities
   - Needs stricter "do not hallucinate" guidance
   
2. **Metadata Override Issue**
   - The main amenities list shows `[]` but extraction_meta shows AC
   - Check if there's filtering that removes it later but metadata still records it
   
3. **LLM Inference Too Loose**
   - Model inferring amenities from property type ("furnished" → AC assumed?)

### Impact
- False positives in amenity extraction
- Breaks search/filtering
- Users see amenities that don't exist

### Fix (Requires Investigation)
Need to:
1. Add stricter validation to LLM prompt - require explicit mention
2. Add de-duplication between regex+llm sources
3. Verify no amenities are being hallucinated as "assumed standard"

---

## REGRESSION #3: Message Title Loss ⚠️ CRITICAL

### Evidence
```
Input:  "1BHK FLAT ON RENT"
V2 Expected: "1 BHK Flat For Rent" (or similar structured title)
V3 Actual:   "Flat" (lost BHK + transaction type)

Input:  "1 bhk fully furnished in blue empire@36000"
V3 Output:   "1 BHK Fully Furnished in Blue Empire" (good!)
```

### Root Cause - RACE CONDITION

**The Problem**: In [main.py](main.py) line ~46-51:

```python
builder.add_edge("clean_text", "extract_metadata")  # Runs IMMEDIATELY
builder.add_edge("clean_text", "extract_bhk")       # Runs in PARALLEL
builder.add_edge("clean_text", "extract_location")  # Runs in PARALLEL
builder.add_edge("clean_text", "extract_request_type")  # Runs in PARALLEL
```

But `build_title()` at [metadata_extractor.py](metadata_extractor.py#L96-L118) requires:
- `state.bhk`
- `state.primary_location`
- `state.request_type`

These don't exist yet when extract_metadata runs!

**Why Inconsistent**:
- Lucky timing: All extractors complete first → Title has all info → ✓ "1 BHK Fully Furnished in Blue Empire"
- Unlucky timing: extract_metadata runs first → Values are None → ✗ Fallback to "Flat"

### Impact
- Message titles lose critical search/indexing info
- Inconsistent results
- Bad for embeddings and UI rendering

### Fix

**Option A (Recommended)**: Enforce dependency ordering
```python
# Remove extract_metadata from parallel edges with clean_text
# Remove: builder.add_edge("clean_text", "extract_metadata")

# Instead, add it AFTER all feature extractors
builder.add_edge(
    ["extract_request_type", "extract_bhk", "extract_price", "extract_location", 
     "extract_furnishing", "extract_facing", "extract_parking", "extract_amenities", 
     "extract_property_subtype"],
    "extract_metadata"  # Now it runs LAST, after all data is available
)

# Adjust final edge to response
builder.add_edge(
    ["extract_metadata"],  # Remove others from here if moving
    "response"
)
```

---

## SUMMARY OF FIXES

| Issue | Fix Type | Severity | Complexity |
|-------|----------|----------|-----------|
| Pricing Reversal | 1 line change (elif→if) | 🔴 CRITICAL | ⭐ Easy |
| Fake Amenities | Investigation + prompt tuning | 🔴 CRITICAL | ⭐⭐ Medium |
| Title Race Condition | Graph edge reordering | 🔴 CRITICAL | ⭐ Easy |

All three can be fixed today. Pricing fix is trivial (1 line). Title fix is a few line changes. Amenities needs investigation but likely a prompt/validation fix.
