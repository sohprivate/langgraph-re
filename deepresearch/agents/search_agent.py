import os
import requests
from typing import Any, Dict, List

class SearchAgent:
    """Agent for retrieving relevant documents using Tavily Search API."""

    BASE_URL = "https://api.tavily.com/search"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not provided")

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        params = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
        }
        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
