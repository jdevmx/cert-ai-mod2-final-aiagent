"""Conversation service — reads and writes the Firestore ``conversations`` collection.

Uses the Nullable Infrastructure pattern: the storage adapter is
injected so tests can substitute an in-memory stub.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Protocol

from models.chat import ConversationMessage

logger = logging.getLogger(__name__)


class ConversationPort(Protocol):
    """Minimal interface required by ConversationService."""

    def get(self, user_id: str) -> list[dict[str, Any]]: ...
    def append(self, user_id: str, message: dict[str, Any]) -> None: ...
    def clear(self, user_id: str) -> None: ...


class FirestoreConversationDb:
    """Production adapter — wraps the real Firestore client."""

    def __init__(self, db: Any) -> None:
        self._db = db

    def get(self, user_id: str) -> list[dict[str, Any]]:
        doc = self._db.collection("conversations").document(user_id).get()
        if not doc.exists:
            return []
        return doc.to_dict().get("messages", [])

    def append(self, user_id: str, message: dict[str, Any]) -> None:
        from firebase_admin import firestore as fs

        ref = self._db.collection("conversations").document(user_id)
        ref.set(
            {
                "user_id": user_id,
                "messages": fs.ArrayUnion([message]),
                "updated_at": datetime.now(timezone.utc),
            },
            merge=True,
        )

    def clear(self, user_id: str) -> None:
        ref = self._db.collection("conversations").document(user_id)
        ref.set(
            {"user_id": user_id, "messages": [], "updated_at": datetime.now(timezone.utc)},
            merge=True,
        )


class ConversationService:
    def __init__(self, db: ConversationPort) -> None:
        self._db = db

    def get_messages(self, user_id: str) -> list[ConversationMessage]:
        """Return all stored messages for a user (empty list if none)."""
        raw = self._db.get(user_id)
        return [ConversationMessage(**m) for m in raw]

    def append_message(self, user_id: str, role: str, content: str) -> None:
        """Append a single human or AI message to the conversation."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._db.append(user_id, message)
        logger.debug("Appended %s message for user %s", role, user_id)

    def clear_messages(self, user_id: str) -> None:
        """Delete all messages for a user (reset conversation)."""
        self._db.clear(user_id)
        logger.info("Cleared conversation for user %s", user_id)
