import re
from typing import Any, Tuple, Optional
from extractor.GraphState import GraphState

class ExtractionRule:
    """Base class for all extraction rules."""
    def name(self) -> str:
        return self.__class__.__name__

    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_passed, failure_message).
        """
        raise NotImplementedError


class RentMustBeLessThanDeposit(ExtractionRule):
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        if state.rent_price is not None and state.deposit_price is not None:
            if state.rent_price > state.deposit_price:
                return False, f"Rent price ({state.rent_price}) cannot be greater than deposit price ({state.deposit_price})."
        return True, None


class PriceMinMustBeLessThanPriceMax(ExtractionRule):
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        if state.price_min is not None and state.price_max is not None:
            if state.price_min > state.price_max:
                return False, f"Price min ({state.price_min}) cannot be greater than price max ({state.price_max})."
        return True, None


class BHKMustMatchTitle(ExtractionRule):
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        if state.bhk is not None and state.message_title:
            expected = f"{state.bhk}bhk"
            title_lower = state.message_title.lower().replace(" ", "")
            if expected not in title_lower:
                return False, f"BHK ({state.bhk}) does not match message title '{state.message_title}'."
        return True, None


class CommercialCannotHaveBHK(ExtractionRule):
    COMMERCIAL_TYPES = {
        "office", "coworking", "shop", "showroom", "commercial_space",
        "warehouse", "industrial_shed", "gala", "plot", "land"
    }
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        if state.property_subtype in self.COMMERCIAL_TYPES and state.bhk is not None:
            return False, f"Commercial property subtype '{state.property_subtype}' cannot have a BHK value."
        return True, None


class FullyFurnishedShouldNotInferAC(ExtractionRule):
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        # Fully furnished furnishing status should not automatically add AC as amenity
        # unless 'ac' or 'air conditioning' is explicitly in source text
        if state.amenities and "air conditioning" in state.amenities:
            source = (state.user_input or state.cleaned_text or "").lower()
            if not re.search(r"\bac\b|\bair\s*condition", source):
                return False, "Air conditioning amenity cannot be inferred unless explicitly mentioned in source."
        return True, None


class PriceRangeConsistentWithRequestType(ExtractionRule):
    def evaluate(self, state: GraphState) -> Tuple[bool, Optional[str]]:
        req_type = state.request_type
        # If rent, price should not be a purchase price (> 5,000,000 INR)
        if req_type == "rent" and state.price is not None and state.price >= 5_000_000:
            return False, f"Rent price ({state.price}) is abnormally high (>= 5,000,000 INR)."
        # If sale, price should not be a rent price (< 500,000 INR)
        if req_type == "sale" and state.price is not None and state.price < 500_000:
            return False, f"Sale price ({state.price}) is abnormally low (< 500,000 INR)."
        return True, None


# Registry of active rules
RULES = [
    RentMustBeLessThanDeposit(),
    PriceMinMustBeLessThanPriceMax(),
    BHKMustMatchTitle(),
    CommercialCannotHaveBHK(),
    FullyFurnishedShouldNotInferAC(),
    PriceRangeConsistentWithRequestType(),
]


def run_rule_engine(state: GraphState) -> Tuple[bool, list[str]]:
    """Runs all registry rules on the state. Returns (is_all_valid, list of failure reasons)."""
    failures = []
    for rule in RULES:
        passed, error = rule.evaluate(state)
        if not passed:
            failures.append(f"{rule.name()}: {error}")
    return len(failures) == 0, failures


def get_rule_failed_fields(rule_name: str) -> list[str]:
    mapping = {
        "RentMustBeLessThanDeposit": ["pricing.rent_price", "pricing.deposit_price"],
        "PriceMinMustBeLessThanPriceMax": ["pricing.price_min", "pricing.price_max"],
        "BHKMustMatchTitle": ["summary.bhk", "metadata.message_title"],
        "CommercialCannotHaveBHK": ["summary.bhk", "property.property_subtype"],
        "FullyFurnishedShouldNotInferAC": ["amenities"],
        "PriceRangeConsistentWithRequestType": ["pricing.price", "summary.request_type"]
    }
    return mapping.get(rule_name, [])
