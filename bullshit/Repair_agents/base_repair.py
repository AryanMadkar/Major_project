# repair/base_repair.py

from pydantic import BaseModel
from typing import Any, Optional


class RepairResult(BaseModel):

    field_name: str

    old_value: Any = None

    new_value: Any = None

    confidence: int

    is_repaired: bool

    evidence: Optional[str] = None

    issue: Optional[str] = None

    repair_agent: str