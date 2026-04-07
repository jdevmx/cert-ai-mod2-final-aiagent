"""Unit tests for the system prompt builder."""

from __future__ import annotations

from models.user import UserProfile
from agent.prompt import build_system_prompt


def _make_profile(**overrides) -> UserProfile:
    defaults = dict(
        user_id="u1",
        display_name="Test User",
        email="test@example.com",
        vehicle="2022 Toyota 4Runner TRD Pro",
        lift_height_in=3.0,
        tire_size="285/70R17",
        locking_diffs=True,
        primary_use="overlanding",
        skill_level="intermediate",
    )
    defaults.update(overrides)
    return UserProfile(**defaults)


def test_prompt_contains_vehicle():
    profile = _make_profile(vehicle="2021 Ford Bronco Wildtrak")
    prompt = build_system_prompt(profile)
    assert "2021 Ford Bronco Wildtrak" in prompt


def test_prompt_contains_tire_size():
    profile = _make_profile(tire_size="35x12.50R17")
    prompt = build_system_prompt(profile)
    assert "35x12.50R17" in prompt


def test_prompt_mentions_locking_diffs_yes():
    profile = _make_profile(locking_diffs=True)
    prompt = build_system_prompt(profile)
    assert "yes" in prompt


def test_prompt_mentions_locking_diffs_no():
    profile = _make_profile(locking_diffs=False)
    prompt = build_system_prompt(profile)
    assert "no" in prompt


def test_prompt_contains_skill_level():
    profile = _make_profile(skill_level="expert")
    prompt = build_system_prompt(profile)
    assert "expert" in prompt


def test_prompt_stock_lift_description():
    profile = _make_profile(lift_height_in=0.0)
    prompt = build_system_prompt(profile)
    assert "stock" in prompt


def test_prompt_contains_primary_use():
    profile = _make_profile(primary_use="trail")
    prompt = build_system_prompt(profile)
    assert "trail" in prompt
