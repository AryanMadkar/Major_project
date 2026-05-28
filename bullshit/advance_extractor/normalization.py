import re
from typing import Any
from extractor.GraphState import GraphState

def normalize_prices(state: GraphState) -> None:
    """Standardize price values and formats."""
    # Ensure all prices are canonical integers or None
    for field in ["price", "price_min", "price_max", "rent_price", "deposit_price"]:
        val = getattr(state, field)
        if val is not None:
            try:
                setattr(state, field, int(float(val)))
            except (ValueError, TypeError):
                setattr(state, field, None)

    # Apply range sanity: price_min must be <= price_max
    if state.price_min is not None and state.price_max is not None:
        if state.price_min > state.price_max:
            # Swap them
            state.price_min, state.price_max = state.price_max, state.price_min


def normalize_locations(state: GraphState) -> None:
    """Normalize location entries and deduplicate."""
    if not state.locations:
        state.locations = []
        state.primary_location = None
        return

    normalized = []
    seen = set()
    for loc in state.locations:
        if not loc:
            continue
        cleaned = re.sub(r"\s+", " ", str(loc).strip().lower())
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            normalized.append(cleaned)

    state.locations = normalized
    state.primary_location = normalized[0] if normalized else None


def normalize_amenities(state: GraphState) -> None:
    """Deduplicate and sort amenities."""
    if not state.amenities:
        state.amenities = []
        return

    normalized = []
    seen = set()
    for am in state.amenities:
        if not am:
            continue
        cleaned = re.sub(r"\s+", " ", str(am).strip().lower())
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            normalized.append(cleaned)

    state.amenities = sorted(normalized)


def run_normalization_pipeline(state: GraphState) -> GraphState:
    """Run all normalization functions in sequence."""
    normalize_prices(state)
    normalize_locations(state)
    normalize_amenities(state)
    return state
