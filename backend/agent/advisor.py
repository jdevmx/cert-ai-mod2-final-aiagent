"""LangChain ReAct agent factory for the 4x4 Off-Road Advisor.

``build_advisor_agent()`` is a factory — not a module-level singleton —
so tests can inject a stub LLM and stub search tool without any real
API calls.
"""

from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from config import settings

logger = logging.getLogger(__name__)

# ReAct prompt template required by create_react_agent
_REACT_TEMPLATE = """{system_prompt}

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

{chat_history}
Question: {input}
Thought:{agent_scratchpad}"""


def build_advisor_agent(
    system_prompt: str,
    tools: list[BaseTool] | None = None,
    llm: Any | None = None,
) -> AgentExecutor:
    """Return a configured AgentExecutor.

    Parameters
    ----------
    system_prompt:
        Pre-built system prompt (with rig profile interpolated).
    tools:
        List of LangChain tools. Defaults to the Tavily search tool.
    llm:
        LangChain chat model. Defaults to GPT-4o with streaming enabled.
    """
    if tools is None:
        from agent.tools.search import build_search_tool

        tools = [build_search_tool()]

    if llm is None:
        llm = ChatOpenAI(
            model="gpt-4o",
            streaming=True,
            openai_api_key=settings.openai_api_key,
        )

    from langchain_core.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(
        _REACT_TEMPLATE.replace("{system_prompt}", system_prompt)
    )

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=8,
    )


async def stream_agent_response(
    executor: AgentExecutor,
    user_message: str,
    history: list[dict[str, str]],
) -> AsyncIterator[str]:
    """Yield token strings from the agent for the given user message.

    ``history`` is a list of ``{"role": "human"|"ai", "content": "..."}``
    dicts loaded from Firestore.
    """
    chat_history: list[HumanMessage | AIMessage] = []
    for msg in history:
        if msg["role"] == "human":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))

    collected: list[str] = []

    async for event in executor.astream_events(
        {"input": user_message, "chat_history": chat_history},
        version="v1",
    ):
        if event["event"] == "on_llm_stream":
            chunk = event["data"].get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                collected.append(chunk.content)
                yield chunk.content

    if not collected:
        # Fallback: yield the final output if streaming produced nothing
        result = await executor.ainvoke(
            {"input": user_message, "chat_history": chat_history}
        )
        output = result.get("output", "")
        yield output
