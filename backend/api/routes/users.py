"""User profile and conversation history routes.

GET    /api/users/{user_id}/profile        — fetch rig profile
PUT    /api/users/{user_id}/profile        — create/update rig profile
GET    /api/users/{user_id}/conversations  — fetch conversation history
DELETE /api/users/{user_id}/conversations  — clear conversation history
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Response

from firebase_client import get_db
from models.chat import ConversationHistory
from models.user import UserProfile, UserProfileUpdate
from services.conversation import ConversationService, FirestoreConversationDb
from services.user_profile import FirestoreUserProfileDb, UserProfileService

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_services() -> tuple[UserProfileService, ConversationService]:
    db = get_db()
    return (
        UserProfileService(db=FirestoreUserProfileDb(db)),
        ConversationService(db=FirestoreConversationDb(db)),
    )


@router.get("/users/{user_id}/profile", response_model=UserProfile)
async def get_profile(user_id: str) -> UserProfile:
    user_service, _ = _get_services()
    profile = user_service.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


@router.put("/users/{user_id}/profile", response_model=UserProfile)
async def upsert_profile(user_id: str, update: UserProfileUpdate) -> UserProfile:
    user_service, _ = _get_services()
    try:
        return user_service.upsert_profile(user_id, update)
    except Exception as exc:
        logger.error("Failed to upsert profile for %s: %s", user_id, exc)
        raise HTTPException(status_code=500, detail="Failed to save profile") from exc


@router.get("/users/{user_id}/conversations", response_model=ConversationHistory)
async def get_conversations(user_id: str) -> ConversationHistory:
    _, conversation_service = _get_services()
    messages = conversation_service.get_messages(user_id)
    return ConversationHistory(user_id=user_id, messages=messages)


@router.delete("/users/{user_id}/conversations", status_code=204)
async def clear_conversations(user_id: str) -> Response:
    _, conversation_service = _get_services()
    try:
        conversation_service.clear_messages(user_id)
    except Exception as exc:
        logger.error("Failed to clear conversation for %s: %s", user_id, exc)
        raise HTTPException(status_code=500, detail="Failed to clear conversation") from exc
    return Response(status_code=204)
