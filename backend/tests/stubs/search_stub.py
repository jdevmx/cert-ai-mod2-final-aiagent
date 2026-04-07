"""Stub Tavily search tool for agent tests.

Returns a fixed list of results without any network calls.
"""

from __future__ import annotations

from langchain_core.tools import BaseTool


class StubSearchTool(BaseTool):
    """Returns a canned search result list — no HTTP calls."""

    name: str = "tavily_search_results_json"
    description: str = "Stub search tool for tests."
    results: list[dict] = [
        {
            "title": "Best 4x4 Lift Kits 2024",
            "url": "https://example.com/lift-kits",
            "content": "A 3-inch lift kit on a 4Runner typically costs $800–$1,500 installed.",
        }
    ]

    def _run(self, query: str) -> list[dict]:  # type: ignore[override]
        return self.results

    async def _arun(self, query: str) -> list[dict]:  # type: ignore[override]
        return self.results
