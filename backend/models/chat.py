"""Pydantic schemas for chat request/response and conversation history."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    user_id: str
    message: str
    conversation_length: int


class ConversationMessage(BaseModel):
    role: Literal["human", "ai"]
    content: str
    timestamp: datetime | None = None


class ConversationHistory(BaseModel):
    user_id: str
    messages: list[ConversationMessage]
    updated_at: datetime | None = None
