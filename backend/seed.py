"""Seed script — writes 3 rich user profiles to Firestore for testing.

Usage:
    cd backend
    source .venv/bin/activate
    python seed.py

Requires FIREBASE_CREDENTIALS_JSON in .env (base64-encoded service account JSON).
"""

from __future__ import annotations

import logging

from firebase_client import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SEED_PROFILES: list[dict] = [
    {
        "user_id": "user_trail_pro",
        "display_name": "Marcus B.",
        "email": "marcus@example.com",
        "vehicle": "2021 Ford Bronco Wildtrak",
        "lift_height_in": 4.0,
        "tire_size": "35x12.50R17",
        "locking_diffs": True,
        "primary_use": "trail",
        "skill_level": "expert",
    },
    {
        "user_id": "user_overlander",
        "display_name": "Sofia R.",
        "email": "sofia@example.com",
        "vehicle": "2022 Toyota 4Runner TRD Pro",
        "lift_height_in": 3.0,
        "tire_size": "285/70R17",
        "locking_diffs": True,
        "primary_use": "overlanding",
        "skill_level": "intermediate",
    },
    {
        "user_id": "user_weekend_warrior",
        "display_name": "Derek T.",
        "email": "derek@example.com",
        "vehicle": "2020 Jeep Wrangler JL Sport",
        "lift_height_in": 2.0,
        "tire_size": "265/70R17",
        "locking_diffs": False,
        "primary_use": "trail",
        "skill_level": "beginner",
    },
]


def seed() -> None:
    db = get_db()

    for profile in SEED_PROFILES:
        user_id = profile.pop("user_id")
        db.collection("users").document(user_id).set(profile, merge=True)
        logger.info("Seeded profile for %s (%s)", user_id, profile["display_name"])

    logger.info("Seed complete — %d profiles written.", len(SEED_PROFILES))


if __name__ == "__main__":
    seed()
