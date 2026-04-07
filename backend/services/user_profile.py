"""User profile service — reads and writes the Firestore ``users`` collection.

Follows the Nullable Infrastructure pattern: the Firestore client is
injected via the constructor so tests can pass an in-memory stub without
any network I/O.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Protocol

from models.user import UserProfile, UserProfileUpdate

logger = logging.getLogger(__name__)


class UserProfilePort(Protocol):
    """Minimal Firestore-document interface required by this service."""

    def get(self, user_id: str) -> dict[str, Any] | None: ...
    def set(self, user_id: str, data: dict[str, Any]) -> None: ...


class FirestoreUserProfileDb:
    """Production adapter — wraps the real Firestore client."""

    def __init__(self, db: Any) -> None:
        self._db = db

    def get(self, user_id: str) -> dict[str, Any] | None:
        doc = self._db.collection("users").document(user_id).get()
        return doc.to_dict() if doc.exists else None

    def set(self, user_id: str, data: dict[str, Any]) -> None:
        self._db.collection("users").document(user_id).set(data, merge=True)


class UserProfileService:
    def __init__(self, db: UserProfilePort) -> None:
        self._db = db

    def get_profile(self, user_id: str) -> UserProfile | None:
        """Return the user's rig profile, or ``None`` if it does not exist."""
        data = self._db.get(user_id)
        if data is None:
            return None
        return UserProfile(user_id=user_id, **data)

    def upsert_profile(self, user_id: str, update: UserProfileUpdate) -> UserProfile:
        """Create or update the user's rig profile and return the saved document."""
        now = datetime.now(timezone.utc)
        existing = self._db.get(user_id)
        created_at = existing.get("created_at", now) if existing else now

        data = update.model_dump()
        data["created_at"] = created_at
        data["updated_at"] = now

        self._db.set(user_id, data)
        logger.info("Upserted profile for user %s", user_id)
        return UserProfile(user_id=user_id, **data)
