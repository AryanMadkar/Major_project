# Final Roadmap For Your Extraction System

You already built the **base extraction engine**.
Now do NOT rewrite it.

Your next job is to evolve it into:

```text
Production Grade Self-Healing Extraction System
```

---

# CURRENT STAGE

You already have:

```text
cleaning
→ fast extractors
→ metadata
→ verification
→ structured response
```

Very good foundation.

Now the roadmap ahead is:

---

# PHASE 1 — VERIFICATION-DRIVEN REPAIR SYSTEM

This is your immediate next step.

---

# Step 1 — Add Failed Field Tracking

Add inside `GraphState`:

```python
failed_fields: list[str] | None = None

repair_candidates: list[dict] | None = None

repair_attempts: dict[str, int] | None = None
```

Purpose:

| Field             | Purpose                          |
| ----------------- | -------------------------------- |
| failed_fields     | Which fields failed verification |
| repair_candidates | Suggested repairs                |
| repair_attempts   | Prevent infinite loops           |

---

# Step 2 — Build Verification Aggregator Node

NEW NODE:

```text
aggregate_verification_results
```

This node:

* reads all verifier outputs
* finds incorrect fields
* stores them in state

Example output:

```python
{
    "failed_fields": [
        "summary.bhk",
        "pricing.price"
    ]
}
```

---

# Step 3 — Add Conditional Routing

This is the MOST IMPORTANT PART.

Add:

```python
builder.add_conditional_edges(
    "aggregate_verification_results",
    verification_router,
    {
        "repair": "repair_dispatcher",
        "end": END
    }
)
```

---

# Step 4 — Build Repair Dispatcher

NEW NODE:

```text
repair_dispatcher
```

This decides WHICH repair agents to trigger.

Example:

```python
if "summary.bhk" in failed:
    run bhk_repair

if "pricing.price" in failed:
    run price_repair
```

---

# PHASE 2 — BUILD SPECIALIZED REPAIR AGENTS

This is the core intelligence layer.

---

# You Need These Repair Agents

## 1. BHK Repair Agent

Handles:

* bhk misses
* compact formats
* OCR mistakes

Examples:

```text
2bhk
02 bhk
two bhk
2 bedroom hall kitchen
```

---

## 2. Price Repair Agent

Handles:

* crore/lakh parsing
* phone confusion
* rent vs sale
* range correction

---

## 3. Location Repair Agent

Handles:

* locality extraction
* railway line inference
* spelling variations

---

## 4. Furnishing Repair Agent

Handles:

* implicit furnishing clues
* conflicting furnishing

---

## 5. Amenities Repair Agent

Handles:

* hidden amenities
* shorthand
* typo normalization

---

## 6. Property Type Repair Agent

Handles:

* apartment
* flat
* penthouse
* studio
* villa
* row house

---

# PHASE 3 — STANDARDIZED REPAIR OUTPUT

Every repair agent MUST return the SAME format.

---

# Required Format

```python
{
    "field": "summary.bhk",

    "old_value": None,

    "new_value": 2,

    "confidence": 94,

    "evidence": "2bhk available",

    "repair_agent": "bhk_llm_repair",

    "reason": "regex missed compact format"
}
```

This is critical.

Without standardization your system becomes chaos later.

---

# PHASE 4 — REPAIR MERGE NODE

NEW NODE:

```text
apply_repairs
```

This node decides:

```text
Should repair overwrite state?
```

---

# Merge Rules

## Accept repair ONLY IF:

| Condition               | Required |
| ----------------------- | -------- |
| confidence > threshold  | YES      |
| evidence exists         | YES      |
| not conflicting         | YES      |
| repair attempts < limit | YES      |

---

# Example

```python
if repair["confidence"] >= 85:
    apply
else:
    reject
```

---

# PHASE 5 — REVERIFICATION LOOP

VERY IMPORTANT.

After repairs:

```text
repair
→ reverify only repaired fields
```

NOT full reverification.

Otherwise:

* expensive
* slow
* unnecessary

---

# Flow

```text
verify_bhk
→ bhk_repair
→ reverify_bhk
```

Only localized reverification.

---

# PHASE 6 — ITERATION CONTROL

Critical.

Without this:

* infinite loops
* hallucination cycles

---

# Add Limits

```python
MAX_REPAIR_ATTEMPTS = 2
```

Example:

```python
{
    "summary.bhk": 2,
    "pricing.price": 1
}
```

If exceeded:

```text
mark unresolved
```

---

# PHASE 7 — EXTRACTION CONFIDENCE ENGINE

This makes your system enterprise-grade.

Each extractor should emit:

```python
confidence_score
```

---

# Example

Regex exact match:

```python
95
```

Weak keyword inference:

```python
60
```

LLM repair:

```python
85
```

---

# Final Response Should Include

```json
{
  "value": 2,
  "confidence": 94,
  "verified": true,
  "repaired": true
}
```

This is VERY powerful.

---

# PHASE 8 — EXTRACTION MEMORY SYSTEM

Huge future upgrade.

Store successful repair patterns.

Example:

```text
2br → 2bhk
```

If same pattern appears again:

* auto-fix
* no LLM needed

This creates:

* self-improving system
* lower cost
* faster runtime

---

# PHASE 9 — PARALLEL REPAIR EXECUTION

Your graph should eventually do:

```text
bhk repair
price repair
location repair
```

ALL simultaneously.

LangGraph is excellent for this.

---

# PHASE 10 — HIERARCHICAL VERIFICATION

Later build:

---

## Layer 1 — Field Verification

```text
Is BHK correct?
```

---

## Layer 2 — Cross Field Verification

```text
1 BHK + 12 Cr
```

Suspicious.

---

## Layer 3 — Semantic Consistency

```text
rent + outright sale
```

Conflict.

This is where your system becomes extremely advanced.

---

# FINAL TARGET ARCHITECTURE

Your final production pipeline:

```text
clean_text
    ↓
parallel_fast_extractors
    ↓
metadata_builder
    ↓
parallel_verifiers
    ↓
verification_aggregator
    ↓
conditional_router
    ↓
parallel_repair_agents
    ↓
repair_merge
    ↓
localized_reverification
    ↓
repair_loop_controller
    ↓
final_response_builder
```

---

# YOUR PRIORITY ORDER

Do EXACTLY in this order.

---

# PRIORITY 1

Build:

```text
verification aggregator
conditional router
repair dispatcher
```

This is mandatory first.

---

# PRIORITY 2

Build only:

* bhk repair
* price repair

These give biggest gains.

---

# PRIORITY 3

Build repair merge system.

---

# PRIORITY 4

Build localized reverification.

---

# PRIORITY 5

Add confidence engine.

---

# PRIORITY 6

Add repair memory/cache learning.

---

# MOST IMPORTANT THING

Your architecture philosophy should remain:

```text
FAST RULES FIRST
LLM ONLY FOR FAILURES
VERIFY EVERYTHING
TRACK EVERY CHANGE
```

That is exactly the correct direction for a scalable extraction system.
