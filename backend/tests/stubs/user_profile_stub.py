"""In-memory stub for the UserProfilePort.

No Firestore, no network — instant execution in tests.
"""

from __future__ import annotations

from typing import Any


class InMemoryUserProfileDb:
    """Nullable stub — stores profiles in a plain Python dict."""

    def __init__(self, initial: dict[str, dict[str, Any]] | None = None) -> None:
        self._store: dict[str, dict[str, Any]] = initial or {}

    def get(self, user_id: str) -> dict[str, Any] | None:
        return dict(self._store[user_id]) if user_id in self._store else None

    def set(self, user_id: str, data: dict[str, Any]) -> None:
        self._store[user_id] = dict(data)
