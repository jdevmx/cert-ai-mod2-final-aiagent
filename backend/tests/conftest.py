"""Shared pytest fixtures.

All fixtures use in-memory stubs — no Firestore, no OpenAI, no network.
"""

from __future__ import annotations

import pytest

from models.user import UserProfile
from tests.stubs.conversation_stub import InMemoryConversationDb
from tests.stubs.user_profile_stub import InMemoryUserProfileDb

SAMPLE_PROFILE_DATA: dict = {
    "display_name": "Alex T.",
    "email": "alex@example.com",
    "vehicle": "2022 Toyota 4Runner TRD Pro",
    "lift_height_in": 3.0,
    "tire_size": "285/70R17",
    "locking_diffs": True,
    "primary_use": "overlanding",
    "skill_level": "intermediate",
    "created_at": None,
    "updated_at": None,
}


@pytest.fixture()
def sample_profile() -> UserProfile:
    return UserProfile(user_id="user_abc123", **SAMPLE_PROFILE_DATA)


@pytest.fixture()
def profile_db_with_user() -> InMemoryUserProfileDb:
    return InMemoryUserProfileDb(initial={"user_abc123": SAMPLE_PROFILE_DATA})


@pytest.fixture()
def empty_conversation_db() -> InMemoryConversationDb:
    return InMemoryConversationDb()


@pytest.fixture()
def conversation_db_with_history() -> InMemoryConversationDb:
    return InMemoryConversationDb(
        initial={
            "user_abc123": [
                {"role": "human", "content": "What tire pressure for sand?", "timestamp": None},
                {"role": "ai", "content": "Air down to 15–18 PSI.", "timestamp": None},
            ]
        }
    )
