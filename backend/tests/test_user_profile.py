"""Unit tests for UserProfileService using the in-memory stub."""

from __future__ import annotations

import pytest

from models.user import UserProfileUpdate
from services.user_profile import UserProfileService
from tests.stubs.user_profile_stub import InMemoryUserProfileDb


SAMPLE_UPDATE = UserProfileUpdate(
    display_name="Jordan K.",
    email="jordan@example.com",
    vehicle="2023 Jeep Wrangler Rubicon 392",
    lift_height_in=2.5,
    tire_size="37x12.50R17",
    locking_diffs=True,
    primary_use="trail",
    skill_level="expert",
)


def test_get_profile_returns_none_for_unknown_user():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    assert svc.get_profile("unknown_user") is None


def test_upsert_profile_creates_new_document():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    profile = svc.upsert_profile("u1", SAMPLE_UPDATE)
    assert profile.user_id == "u1"
    assert profile.vehicle == "2023 Jeep Wrangler Rubicon 392"
    assert profile.skill_level == "expert"


def test_upsert_profile_updates_existing_document():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    svc.upsert_profile("u1", SAMPLE_UPDATE)

    update_v2 = SAMPLE_UPDATE.model_copy(update={"lift_height_in": 4.0})
    profile = svc.upsert_profile("u1", update_v2)
    assert profile.lift_height_in == 4.0


def test_upsert_profile_preserves_created_at():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    p1 = svc.upsert_profile("u1", SAMPLE_UPDATE)
    original_created_at = p1.created_at
    p2 = svc.upsert_profile("u1", SAMPLE_UPDATE)
    assert p2.created_at == original_created_at


def test_get_profile_after_upsert_returns_saved_data():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    svc.upsert_profile("u1", SAMPLE_UPDATE)
    profile = svc.get_profile("u1")
    assert profile is not None
    assert profile.display_name == "Jordan K."
    assert profile.locking_diffs is True


def test_profile_stock_lift_is_zero():
    stub = InMemoryUserProfileDb()
    svc = UserProfileService(db=stub)
    stock_update = SAMPLE_UPDATE.model_copy(update={"lift_height_in": 0.0})
    profile = svc.upsert_profile("u1", stock_update)
    assert profile.lift_height_in == 0.0


def test_primary_use_enum_values():
    for use in ("trail", "overlanding", "daily"):
        stub = InMemoryUserProfileDb()
        svc = UserProfileService(db=stub)
        update = SAMPLE_UPDATE.model_copy(update={"primary_use": use})
        profile = svc.upsert_profile("u1", update)
        assert profile.primary_use == use
