from typing import Any

from pydantic import BaseModel


class GraphState(BaseModel):

    # =================================
    # INPUT
    # =================================

    user_input: str | None = None

    cleaned_text: str | None = None

    # =================================
    # PROPERTY DETAILS
    # =================================

    bhk: int | None = None

    property_subtype: str | None = None

    furnishing: str | None = None

    facing: str | None = None

    parking_count: int | None = None

    parking_type: str | None = None

    amenities: list[str] | None = None

    # =================================
    # PRICE
    # =================================

    price: int | None = None

    price_min: int | None = None

    price_max: int | None = None

    rent_price: int | None = None

    deposit_price: int | None = None

    # =================================
    # LOCATION
    # =================================

    locations: list[str] | None = None

    primary_location: str | None = None

    railway_line: str | None = None

    # =================================
    # CONTACT
    # =================================

    contact_people: list[str] | None = None

    contact_numbers: list[str] | None = None

    # =================================
    # REQUEST
    # =================================

    request_type: str | None = None

    # =================================
    # VALIDATION / PIPELINE
    # =================================

    validation_report: dict[str, Any] | None = None

    verification_history: list[dict[str, Any]] | None = None

    iteration_count: int | None = None

    should_continue: bool | None = None

    # =================================
    # EXTRA METADATA
    # =================================

    all_detected_subtypes: list[str] | None = None

    metadata_summary: dict[str, Any] | None = None

    response_output: dict[str, Any] | None = None

    message_title: str | None = None