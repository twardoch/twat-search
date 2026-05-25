# this_file: src/twat_search/web/llm.py
"""OpenAI-compatible LLM helpers for query preparation and ranking."""

from __future__ import annotations

import json
from typing import Any

from twat_search.web.config import LLMConfig
from twat_search.web.llm_transport import LLMError, OpenAICompatibleLLMClient
from twat_search.web.models import SearchAnswer, SearchFailure, SearchResult

DEFAULT_QUERY_REWRITE_PROMPT = (
    "Rewrite the user's web search query for high-recall search. "
    "Return exactly one search query, with no markdown, quotes, or explanation. "
    "Preserve named entities, dates, operators, and quoted phrases."
)
DEFAULT_QUERY_DECOMPOSITION_PROMPT = (
    "Decompose the user's web search query into a small set of high-recall search queries. "
    "Return only JSON: an array of strings. Include the original intent, preserve named entities, "
    "dates, operators, and quoted phrases, and avoid duplicates."
)
DEFAULT_RERANK_PROMPT = (
    "Rerank web search results for relevance to the user's query. "
    "Return only JSON: an array of objects with result_id, score, and rationale. "
    "Use result_id values exactly as provided. Scores must be numbers from 0 to 1."
)
DEFAULT_SYNTHESIS_PROMPT = (
    "Answer the user's query using only the provided search results. "
    "Return only JSON with keys answer and cited_urls. "
    "Every factual claim must be supported by cited_urls from the provided results. "
    "If provider failures are listed, mention that some sources failed."
)
RERANK_PROMPT_VERSION = "twat-search-rerank-v1"
SYNTHESIS_PROMPT_VERSION = "twat-search-synthesis-v1"
DECOMPOSITION_PROMPT_VERSION = "twat-search-decomposition-v1"


def normalize_rewritten_query(value: str) -> str:
    """Normalize a model-produced search query while preserving operators."""
    query = value.strip()
    if len(query) >= 2 and query[0] == query[-1] and query[0] in {"'", '"'}:
        query = query[1:-1].strip()
    return query


def _dedupe_queries(values: list[str], *, fallback: str, limit: int) -> list[str]:
    """Normalize, deduplicate, and cap model-produced query strings."""
    queries: list[str] = []
    for value in [fallback, *values]:
        query = normalize_rewritten_query(str(value))
        if query and query.casefold() not in {existing.casefold() for existing in queries}:
            queries.append(query)
        if len(queries) >= limit:
            break
    return queries or [fallback]


def _json_from_model_text(value: str) -> Any:
    """Parse JSON returned directly or inside a fenced code block."""
    text = value.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)


def _result_payload(result_id: int, result: SearchResult) -> dict[str, Any]:
    """Build a compact, JSON-serializable rerank candidate."""
    return {
        "result_id": result_id,
        "title": result.title,
        "url": str(result.url),
        "snippet": result.snippet,
        "source": result.source,
        "rank": result.rank,
    }


def _failure_payload(failure: SearchFailure) -> dict[str, Any]:
    """Build a compact failure payload for answer synthesis."""
    return {
        "engine": failure.engine,
        "kind": failure.kind,
        "message": failure.message,
        "retryable": failure.retryable,
    }


def _parse_rerank_items(value: str) -> list[dict[str, Any]]:
    """Parse model-produced rerank data into a list of item dicts."""
    data = _json_from_model_text(value)
    if isinstance(data, dict):
        data = data.get("results") or data.get("rankings")
    if not isinstance(data, list):
        msg = "LLM rerank response must be a JSON array or object with results/rankings"
        raise LLMError(msg)

    parsed: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict) or "result_id" not in item:
            continue
        try:
            result_id = int(item["result_id"])
            score = float(item.get("score", 0.0))
        except (TypeError, ValueError):
            continue
        parsed.append(
            {
                "result_id": result_id,
                "score": max(0.0, min(score, 1.0)),
                "rationale": str(item.get("rationale", "")).strip(),
            },
        )
    return parsed


async def rewrite_search_query(
    query: str,
    config: LLMConfig,
    *,
    client: OpenAICompatibleLLMClient | None = None,
) -> str:
    """Rewrite a query with an OpenAI-compatible LLM, falling back when disabled."""
    if not config.query_rewrite:
        return query
    if not config.is_configured():
        msg = "LLM query rewrite requires enabled=true, model, api_key, and base_url"
        raise LLMError(msg)

    llm_client = client or OpenAICompatibleLLMClient(config)
    prompt = config.system_prompt or DEFAULT_QUERY_REWRITE_PROMPT
    rewritten = await llm_client.chat(
        [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ],
    )
    normalized = normalize_rewritten_query(rewritten)
    return normalized or query


async def decompose_search_query(
    query: str,
    config: LLMConfig,
    *,
    client: OpenAICompatibleLLMClient | None = None,
) -> list[str]:
    """Decompose a query with an OpenAI-compatible LLM, falling back when disabled."""
    if not config.query_decomposition:
        return [query]
    if not config.is_configured():
        msg = "LLM query decomposition requires enabled=true, model, api_key, and base_url"
        raise LLMError(msg)

    limit = max(1, config.decomposition_max_queries)
    llm_client = client or OpenAICompatibleLLMClient(config)
    content = await llm_client.chat(
        [
            {"role": "system", "content": DEFAULT_QUERY_DECOMPOSITION_PROMPT},
            {"role": "user", "content": query},
        ],
    )
    data = _json_from_model_text(content)
    if isinstance(data, dict):
        data = data.get("queries") or data.get("search_queries")
    if not isinstance(data, list):
        msg = "LLM query decomposition response must be a JSON array or object with queries/search_queries"
        raise LLMError(msg)
    return _dedupe_queries([str(item) for item in data], fallback=query, limit=limit)


async def rerank_search_results(
    query: str,
    results: list[SearchResult],
    config: LLMConfig,
    *,
    client: OpenAICompatibleLLMClient | None = None,
) -> list[SearchResult]:
    """Rerank search results with an OpenAI-compatible LLM and attach provenance."""
    if not config.result_rerank or not results:
        return results
    if not config.is_configured():
        msg = "LLM result rerank requires enabled=true, model, api_key, and base_url"
        raise LLMError(msg)

    limit = max(1, config.rerank_top_n)
    candidates = results[:limit]
    payload = {
        "query": query,
        "results": [_result_payload(result_id, result) for result_id, result in enumerate(candidates)],
    }
    llm_client = client or OpenAICompatibleLLMClient(config)
    content = await llm_client.chat(
        [
            {"role": "system", "content": DEFAULT_RERANK_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    items = _parse_rerank_items(content)
    if not items:
        return results

    by_id = {item["result_id"]: item for item in items if 0 <= item["result_id"] < len(candidates)}
    ordered_ids = [item["result_id"] for item in sorted(by_id.values(), key=lambda item: item["score"], reverse=True)]
    ordered_ids.extend(result_id for result_id in range(len(candidates)) if result_id not in by_id)
    reranked_candidates: list[SearchResult] = []
    for new_index, result_id in enumerate(ordered_ids, start=1):
        result = candidates[result_id]
        item = by_id.get(result_id, {"score": None, "rationale": ""})
        raw = dict(result.raw or {})
        raw["llm_rerank"] = {
            "model": config.model,
            "prompt_version": RERANK_PROMPT_VERSION,
            "input_result_id": result_id,
            "original_rank": result.rank,
            "score": item["score"],
            "rationale": item["rationale"],
        }
        reranked_candidates.append(result.model_copy(update={"rank": new_index, "raw": raw}))

    return reranked_candidates + results[limit:]


async def synthesize_search_answer(
    query: str,
    results: list[SearchResult],
    failures: list[SearchFailure],
    config: LLMConfig,
    *,
    client: OpenAICompatibleLLMClient | None = None,
) -> SearchAnswer | None:
    """Synthesize a cited answer from search results while preserving failures."""
    if not config.answer_synthesis or not results:
        return None
    if not config.is_configured():
        msg = "LLM answer synthesis requires enabled=true, model, api_key, and base_url"
        raise LLMError(msg)

    limit = max(1, config.synthesis_top_n)
    candidates = results[:limit]
    payload = {
        "query": query,
        "results": [_result_payload(result_id, result) for result_id, result in enumerate(candidates)],
        "source_failures": [_failure_payload(failure) for failure in failures],
    }
    llm_client = client or OpenAICompatibleLLMClient(config)
    content = await llm_client.chat(
        [
            {"role": "system", "content": DEFAULT_SYNTHESIS_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    data = _json_from_model_text(content)
    if not isinstance(data, dict):
        msg = "LLM answer synthesis response must be a JSON object"
        raise LLMError(msg)

    text = str(data.get("answer", "")).strip()
    if not text:
        return None

    allowed_urls = {str(result.url).rstrip("/"): str(result.url) for result in candidates}
    cited_urls: list[str] = []
    raw_citations = data.get("cited_urls", [])
    if isinstance(raw_citations, list):
        for value in raw_citations:
            normalized = str(value).strip().rstrip("/")
            if normalized in allowed_urls and allowed_urls[normalized] not in cited_urls:
                cited_urls.append(allowed_urls[normalized])

    return SearchAnswer(
        text=text,
        cited_urls=cited_urls,
        model=str(config.model),
        prompt_version=SYNTHESIS_PROMPT_VERSION,
        input_result_count=len(candidates),
        source_failures=failures,
    )
