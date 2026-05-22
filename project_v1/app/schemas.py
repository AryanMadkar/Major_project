# =====================================================
# schemas.py — Pydantic response models
#
# FastAPI uses these to validate and serialise the
# JSON responses it sends to the client.
# =====================================================

from typing import List
from pydantic import BaseModel, Field


class ModelVote(BaseModel):
    """
    Result returned by a single verification agent.
    """
    model:        str   # agent identifier: "ecapa" | "titanet" | "optimized"
    score:        float # cosine similarity score in [-1.0, 1.0]
    same_speaker: bool  # True if score >= that model's threshold
    error:        str | None = None  # populated only if the agent crashed


class VerificationResponse(BaseModel):
    """
    Top-level API response for POST /verify.
    """
    # True if at least 2 out of 3 models agree it's the same speaker
    final_decision: bool = Field(
        ...,
        description="True = same speaker (majority vote)"
    )

    # Average cosine similarity across all models
    confidence: float = Field(
        ...,
        ge=-1.0, le=1.0,
        description="Average similarity score across models"
    )

    # Per-model breakdown so callers can inspect individual decisions
    votes: List[ModelVote] = Field(
        ...,
        description="Individual results from each model"
    )