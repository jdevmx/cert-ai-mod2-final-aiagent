"""Unit tests for the advisor agent factory using stub LLM and search tool.

No OpenAI calls — the StubLLM returns a canned response immediately.
"""

from __future__ import annotations

import pytest

from agent.advisor import build_advisor_agent, stream_agent_response
from agent.prompt import build_system_prompt
from models.user import UserProfile
from tests.stubs.llm_stub import StubLLM
from tests.stubs.search_stub import StubSearchTool


def _make_profile() -> UserProfile:
    return UserProfile(
        user_id="u1",
        display_name="Test User",
        email="test@example.com",
        vehicle="2022 Toyota 4Runner TRD Pro",
        lift_height_in=3.0,
        tire_size="285/70R17",
        locking_diffs=True,
        primary_use="overlanding",
        skill_level="intermediate",
    )


def test_build_advisor_agent_returns_executor():
    profile = _make_profile()
    system_prompt = build_system_prompt(profile)
    executor = build_advisor_agent(
        system_prompt=system_prompt,
        llm=StubLLM(),
        tools=[StubSearchTool()],
    )
    assert executor is not None


@pytest.mark.asyncio
async def test_stream_agent_response_yields_output():
    profile = _make_profile()
    system_prompt = build_system_prompt(profile)
    stub_llm = StubLLM(response="Final Answer: Air down to 15 PSI for sand driving.")
    executor = build_advisor_agent(
        system_prompt=system_prompt,
        llm=stub_llm,
        tools=[StubSearchTool()],
    )

    tokens: list[str] = []
    async for token in stream_agent_response(executor, "Tire pressure for sand?", []):
        tokens.append(token)

    full_response = "".join(tokens)
    assert len(full_response) > 0


@pytest.mark.asyncio
async def test_stream_agent_response_with_history():
    profile = _make_profile()
    system_prompt = build_system_prompt(profile)
    stub_llm = StubLLM(response="Final Answer: Use 0W-20 full synthetic.")
    executor = build_advisor_agent(
        system_prompt=system_prompt,
        llm=stub_llm,
        tools=[StubSearchTool()],
    )

    history = [
        {"role": "human", "content": "What tire size should I run?"},
        {"role": "ai", "content": "285/70R17 is a great choice for your 4Runner."},
    ]

    tokens: list[str] = []
    async for token in stream_agent_response(executor, "What oil should I use?", history):
        tokens.append(token)

    assert len(tokens) > 0
