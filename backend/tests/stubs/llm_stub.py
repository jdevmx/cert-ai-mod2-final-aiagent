"""Stub LLM for agent tests.

Returns a fixed response string synchronously without any OpenAI calls.
Implements the minimal LangChain BaseChatModel interface used by
``create_react_agent`` and ``AgentExecutor``.
"""

from __future__ import annotations

from typing import Any, Iterator, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class StubLLM(BaseChatModel):
    """Returns a canned ``Final Answer`` so the agent terminates immediately."""

    response: str = "Final Answer: This is a stub response for testing."

    @property
    def _llm_type(self) -> str:
        return "stub"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=self.response))]
        )
