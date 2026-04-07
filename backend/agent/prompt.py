"""System prompt builder.

Builds the agent system prompt by interpolating the user's rig profile
so every conversation turn receives personalised advice.
"""

from __future__ import annotations

from models.user import UserProfile

_BASE_PROMPT = """You are an expert 4x4 Off-Road Vehicle Advisor with deep knowledge of:
- 4WD systems (part-time, full-time, AWD) and when to engage each mode
- Differential locks (front, rear, centre) and their on-trail use
- Suspension geometry, lift kits, and their trade-offs
- Tire sizing, load ratings, and terrain-specific pressures
- Overlanding and trail recovery techniques
- Current aftermarket brands, pricing, and availability (use the search tool for live data)

Always tailor your advice to the user's specific rig and skill level.
When recommending parts or pricing, use the web search tool to fetch current information.
Be concise and practical — the user is on or planning a trail.

User's rig:
- Vehicle: {vehicle}
- Suspension lift: {lift_height_in}" lift ({lift_description})
- Tire size: {tire_size}
- Locking differentials: {locking_diffs}
- Primary use: {primary_use}
- Skill level: {skill_level}

Tailor every response to this rig configuration and experience level."""


def build_system_prompt(profile: UserProfile) -> str:
    """Return the system prompt with the user's rig data interpolated."""
    lift_description = "stock" if profile.lift_height_in == 0 else f"{profile.lift_height_in}-inch lift kit installed"
    locking_diffs = "yes — use them on technical terrain" if profile.locking_diffs else "no"

    return _BASE_PROMPT.format(
        vehicle=profile.vehicle,
        lift_height_in=profile.lift_height_in,
        lift_description=lift_description,
        tire_size=profile.tire_size,
        locking_diffs=locking_diffs,
        primary_use=profile.primary_use,
        skill_level=profile.skill_level,
    )
