import os
from typing import Any, Dict

import openai

class ReportAgent:
    """Agent that summarizes insights using an LLM."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided")
        self.model = model
        openai.api_key = self.api_key

    def summarize(self, analysis: str, search_results: list[dict[str, Any]]) -> str:
        docs = "\n".join(r.get("title", "") + "\n" + r.get("url", "") for r in search_results)
        prompt = (
            "You are a research assistant summarizing weather data insights.\n"
            f"Analysis:\n{analysis}\n\nRelevant documents:\n{docs}\n\n"
            "Provide a concise summary in Japanese."
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"].strip()
