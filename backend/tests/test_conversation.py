"""Unit tests for ConversationService using the in-memory stub."""

from __future__ import annotations

import pytest

from services.conversation import ConversationService
from tests.stubs.conversation_stub import InMemoryConversationDb


def test_get_messages_returns_empty_for_new_user():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    assert svc.get_messages("new_user") == []


def test_append_human_message():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="human", content="What oil does my 4Runner need?")
    messages = svc.get_messages("u1")
    assert len(messages) == 1
    assert messages[0].role == "human"
    assert messages[0].content == "What oil does my 4Runner need?"


def test_append_ai_message():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="ai", content="Use 0W-20 full synthetic.")
    messages = svc.get_messages("u1")
    assert messages[0].role == "ai"
    assert messages[0].content == "Use 0W-20 full synthetic."


def test_multiple_messages_preserve_order():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="human", content="First message")
    svc.append_message("u1", role="ai", content="Second message")
    svc.append_message("u1", role="human", content="Third message")
    messages = svc.get_messages("u1")
    assert len(messages) == 3
    assert messages[0].content == "First message"
    assert messages[2].content == "Third message"


def test_clear_messages_resets_history():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="human", content="Hello")
    svc.append_message("u1", role="ai", content="Hi there")
    svc.clear_messages("u1")
    assert svc.get_messages("u1") == []


def test_messages_are_isolated_per_user():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="human", content="User 1 message")
    svc.append_message("u2", role="human", content="User 2 message")
    assert len(svc.get_messages("u1")) == 1
    assert len(svc.get_messages("u2")) == 1
    assert svc.get_messages("u1")[0].content == "User 1 message"


def test_clear_does_not_affect_other_users():
    stub = InMemoryConversationDb()
    svc = ConversationService(db=stub)
    svc.append_message("u1", role="human", content="User 1 message")
    svc.append_message("u2", role="human", content="User 2 message")
    svc.clear_messages("u1")
    assert svc.get_messages("u1") == []
    assert len(svc.get_messages("u2")) == 1
