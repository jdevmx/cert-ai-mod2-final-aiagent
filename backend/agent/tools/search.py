"""Tavily web-search tool wrapper for the LangChain agent.

Exposes ``build_search_tool()`` so the agent factory can inject a real
or stub search tool depending on the environment.
"""

from __future__ import annotations

from langchain_community.tools.tavily_search import TavilySearchResults

from config import settings


def build_search_tool() -> TavilySearchResults:
    """Return a configured Tavily search tool (max 5 results)."""
    return TavilySearchResults(
        max_results=5,
        tavily_api_key=settings.tavily_api_key,
        description=(
            "Search the web for current 4x4 parts pricing, trail conditions, "
            "product reviews, and brand/model information. "
            "Use this for any question about specific products or live data."
        ),
    )
