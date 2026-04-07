"""Pydantic schemas for user rig profile."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


PrimaryUse = Literal["trail", "overlanding", "daily"]
SkillLevel = Literal["beginner", "intermediate", "expert"]


class UserProfileUpdate(BaseModel):
    """Request body for creating or updating a rig profile."""

    display_name: str = Field(..., min_length=1)
    email: EmailStr
    vehicle: str = Field(..., min_length=1)
    lift_height_in: float = Field(..., ge=0)
    tire_size: str = Field(..., min_length=1)
    locking_diffs: bool
    primary_use: PrimaryUse
    skill_level: SkillLevel


class UserProfile(UserProfileUpdate):
    """Full rig profile including server-assigned metadata."""

    user_id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
