"""Firebase Admin SDK singleton initialisation.

Decodes the base64-encoded service account JSON from the environment,
initialises the Firebase app once, and exposes a ``get_db()`` factory
that returns a Firestore client.  Calling ``get_db()`` multiple times
is safe — the client is cached after the first call.
"""

from __future__ import annotations

import base64
import json
import logging
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

from config import settings

logger = logging.getLogger(__name__)

_db: Any = None


def _load_credentials() -> credentials.Certificate:
    """Decode the base64 service-account JSON and build a Certificate."""
    raw = base64.b64decode(settings.firebase_credentials_json).decode("utf-8")
    service_account_info = json.loads(raw)
    return credentials.Certificate(service_account_info)


def get_db() -> Any:
    """Return the Firestore client, initialising Firebase on first call."""
    global _db
    if _db is None:
        if not firebase_admin._apps:  # avoid double-init in tests
            cred = _load_credentials()
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialised")
        _db = firestore.client()
    return _db
