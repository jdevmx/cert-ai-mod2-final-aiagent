"""Chat API routes.

POST /api/chat        — non-streaming, returns full response as JSON
GET  /api/chat/stream — streaming via Server-Sent Events (SSE)
"""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from agent.advisor import build_advisor_agent, stream_agent_response
from agent.prompt import build_system_prompt
from firebase_client import get_db
from models.chat import ChatRequest, ChatResponse
from services.conversation import ConversationService, FirestoreConversationDb
from services.user_profile import FirestoreUserProfileDb, UserProfileService

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_services() -> tuple[UserProfileService, ConversationService]:
    db = get_db()
    user_service = UserProfileService(db=FirestoreUserProfileDb(db))
    conversation_service = ConversationService(db=FirestoreConversationDb(db))
    return user_service, conversation_service


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Send a message and receive the full agent response as JSON."""
    user_service, conversation_service = _get_services()

    profile = user_service.get_profile(request.user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")

    history = [m.model_dump() for m in conversation_service.get_messages(request.user_id)]

    try:
        system_prompt = build_system_prompt(profile)
        executor = build_advisor_agent(system_prompt=system_prompt)
        tokens: list[str] = []
        async for token in stream_agent_response(executor, request.message, history):
            tokens.append(token)
        full_response = "".join(tokens)
    except Exception as exc:
        logger.error("Agent error for user %s: %s", request.user_id, exc)
        raise HTTPException(status_code=500, detail="Agent error") from exc

    conversation_service.append_message(request.user_id, role="human", content=request.message)
    conversation_service.append_message(request.user_id, role="ai", content=full_response)

    messages = conversation_service.get_messages(request.user_id)
    return ChatResponse(
        user_id=request.user_id,
        message=full_response,
        conversation_length=len(messages),
    )


@router.get("/chat/stream")
async def stream_chat(user_id: str, message: str) -> StreamingResponse:
    """Stream the agent response token-by-token via SSE."""
    if not user_id or not message:
        raise HTTPException(status_code=400, detail="user_id and message are required")

    user_service, conversation_service = _get_services()

    profile = user_service.get_profile(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")

    history = [m.model_dump() for m in conversation_service.get_messages(user_id)]

    async def event_generator():
        collected: list[str] = []
        try:
            system_prompt = build_system_prompt(profile)
            executor = build_advisor_agent(system_prompt=system_prompt)
            async for token in stream_agent_response(executor, message, history):
                collected.append(token)
                yield f"data: {token}\n\n"

            full_response = "".join(collected)
            conversation_service.append_message(user_id, role="human", content=message)
            conversation_service.append_message(user_id, role="ai", content=full_response)

            yield "event: done\ndata: {}\n\n"
        except Exception as exc:
            logger.error("Streaming error for user %s: %s", user_id, exc)
            error_payload = json.dumps({"detail": str(exc)})
            yield f"event: error\ndata: {error_payload}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
