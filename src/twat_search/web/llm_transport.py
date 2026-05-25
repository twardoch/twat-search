# this_file: src/twat_search/web/llm_transport.py
"""OpenAI-compatible LLM transport client."""

from __future__ import annotations

from typing import Any

import httpx

from twat_search.web.config import LLMConfig


class LLMError(RuntimeError):
    """Raised when an LLM-assisted search step cannot produce a usable value."""


class OpenAICompatibleLLMClient:
    """Minimal async client for OpenAI-compatible chat completion endpoints."""

    def __init__(self, config: LLMConfig) -> None:
        """Create a client from validated LLM configuration."""
        if not config.is_configured():
            msg = "LLM config requires enabled=true, model, api_key, and base_url"
            raise LLMError(msg)
        self.config = config

    async def chat(self, messages: list[dict[str, str]]) -> str:
        """Return the first assistant message from a chat completion response."""
        url = f"{str(self.config.base_url).rstrip('/')}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            msg = "LLM chat completion response did not contain choices[0].message.content"
            raise LLMError(msg) from exc

        if not isinstance(content, str):
            msg = "LLM chat completion content must be a string"
            raise LLMError(msg)
        return content
