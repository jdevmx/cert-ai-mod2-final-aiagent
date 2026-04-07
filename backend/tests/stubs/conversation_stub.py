"""In-memory stub for the ConversationPort.

No Firestore, no network — instant execution in tests.
"""

from __future__ import annotations

from typing import Any


class InMemoryConversationDb:
    """Nullable stub — stores messages in a plain Python dict."""

    def __init__(self, initial: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self._store: dict[str, list[dict[str, Any]]] = initial or {}

    def get(self, user_id: str) -> list[dict[str, Any]]:
        return list(self._store.get(user_id, []))

    def append(self, user_id: str, message: dict[str, Any]) -> None:
        self._store.setdefault(user_id, []).append(message)

    def clear(self, user_id: str) -> None:
        self._store[user_id] = []
