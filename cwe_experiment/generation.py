"""Asynchronous OpenAI-compatible generation adapters."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
import os
import random
import re
import time
from typing import Any, Callable, Iterable, Literal


APIKind = Literal["chat-completions", "responses"]
REASONING_SETTINGS = {
    "none",
    "off",
    "on",
    "minimal",
    "low",
    "medium",
    "high",
    "xhigh",
}
_PYTHON_FENCE = re.compile(
    r"```(?:python|py)\s*\r?\n(?P<code>.*?)```", re.IGNORECASE | re.DOTALL
)
_THINK = re.compile(r"<think>(?P<reasoning>.*?)</think>", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class GenerationInput:
    prompt: str
    generation_index: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    generation_index: int
    raw_response: str = ""
    code: str = ""
    reasoning_native: str = ""
    reasoning_extracted: str = ""
    reasoning_summaries: list[dict[str, str]] = field(default_factory=list)
    latency_ms: float = 0.0
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    reasoning_tokens: int | None = None
    status: str = "ok"
    error: str | None = None
    attempts: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)


def _content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue
            if isinstance(block, dict):
                value = block.get("text") or block.get("content")
            else:
                value = getattr(block, "text", None) or getattr(block, "content", None)
            if value:
                parts.append(str(value))
        return "\n".join(parts)
    return str(content)


def extract_think(text: str) -> tuple[str, str]:
    """Return visible answer and concatenated non-standard ``<think>`` blocks."""

    blocks = [match.group("reasoning").strip() for match in _THINK.finditer(text)]
    visible = _THINK.sub("", text).strip()
    return visible, "\n\n".join(block for block in blocks if block)


def extract_code(text: str) -> str:
    """Extract the first Python fence, or return unfenced visible text."""

    visible, _ = extract_think(text)
    match = _PYTHON_FENCE.search(visible)
    return (match.group("code") if match else visible).strip()


def _usage_value(usage: Any, *names: str) -> int | None:
    for name in names:
        if isinstance(usage, dict):
            value = usage.get(name)
        else:
            value = getattr(usage, name, None)
        if isinstance(value, int):
            return value
    return None


def _reasoning_token_count(usage: Any) -> int | None:
    for details_name in ("completion_tokens_details", "output_tokens_details"):
        if isinstance(usage, dict):
            details = usage.get(details_name)
        else:
            details = getattr(usage, details_name, None)
        value = _usage_value(details, "reasoning_tokens")
        if value is not None:
            return value
    return None


def _responses_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str):
        return output_text
    parts: list[str] = []
    for item in getattr(response, "output", None) or []:
        item_type = item.get("type") if isinstance(item, dict) else getattr(item, "type", None)
        if item_type != "message":
            continue
        content = item.get("content", []) if isinstance(item, dict) else getattr(item, "content", [])
        for block in content or []:
            block_type = block.get("type") if isinstance(block, dict) else getattr(block, "type", None)
            if block_type in {"output_text", "text"}:
                value = block.get("text", "") if isinstance(block, dict) else getattr(block, "text", "")
                parts.append(str(value))
    return "\n".join(parts)


def _responses_summaries(response: Any) -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for item in getattr(response, "output", None) or []:
        item_type = item.get("type") if isinstance(item, dict) else getattr(item, "type", None)
        if item_type != "reasoning":
            continue
        blocks = item.get("summary", []) if isinstance(item, dict) else getattr(item, "summary", [])
        for block in blocks or []:
            block_type = block.get("type", "summary_text") if isinstance(block, dict) else getattr(block, "type", "summary_text")
            text = block.get("text", "") if isinstance(block, dict) else getattr(block, "text", "")
            summaries.append({"type": str(block_type), "text": str(text)})
    return summaries


class OpenAIGenerator:
    """Fixed-size concurrent-batch adapter with per-request retries."""

    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        api: APIKind = "chat-completions",
        concurrency: int = 10,
        temperature: float | None = 0.8,
        max_tokens: int | None = None,
        retries: int = 2,
        timeout: float = 120.0,
        reasoning_effort: str | None = None,
        client: Any | None = None,
    ) -> None:
        if api not in {"chat-completions", "responses"}:
            raise ValueError(f"API no soportada: {api}")
        if concurrency < 1:
            raise ValueError("concurrency debe ser al menos 1")
        if reasoning_effort is not None and reasoning_effort not in REASONING_SETTINGS:
            raise ValueError(f"Configuración de reasoning no soportada: {reasoning_effort}")
        self.model = model
        self.base_url = base_url
        self.api = api
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retries = retries
        self.timeout = timeout
        self.reasoning_effort = reasoning_effort
        self.concurrency = concurrency
        self._semaphore = asyncio.Semaphore(concurrency)
        if client is None:
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY no está definida")
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=key, base_url=base_url, timeout=timeout)
        self.client = client

    def _common_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"model": self.model}
        if self.temperature is not None:
            params["temperature"] = self.temperature
        return params

    async def _chat(self, prompt: str) -> tuple[str, str, list[dict[str, str]], Any]:
        params = self._common_params()
        params.update(
            messages=[{"role": "user", "content": prompt}],
            timeout=self.timeout,
        )
        if self.max_tokens is not None:
            params["max_tokens"] = self.max_tokens
        if self.reasoning_effort is not None:
            params["reasoning_effort"] = self.reasoning_effort
        response = await self.client.chat.completions.create(**params)
        message = response.choices[0].message
        text = _content_to_text(getattr(message, "content", ""))
        reasoning = _content_to_text(
            getattr(message, "reasoning_content", None)
            or getattr(message, "reasoning", "")
        )
        return text, reasoning, [], getattr(response, "usage", None)

    async def _responses(self, prompt: str) -> tuple[str, str, list[dict[str, str]], Any]:
        params = self._common_params()
        params.update(input=prompt, timeout=self.timeout)
        if self.max_tokens is not None:
            params["max_output_tokens"] = self.max_tokens
        if self.reasoning_effort is not None:
            params["reasoning"] = {"effort": self.reasoning_effort}
        response = await self.client.responses.create(**params)
        return (
            _responses_text(response),
            "",
            _responses_summaries(response),
            getattr(response, "usage", None),
        )

    async def generate(self, request: GenerationInput) -> GenerationResult:
        started = time.perf_counter()
        last_error: Exception | None = None
        async with self._semaphore:
            for attempt in range(1, self.retries + 2):
                try:
                    call = self._chat if self.api == "chat-completions" else self._responses
                    raw, native_reasoning, summaries, usage = await call(request.prompt)
                    _, extracted_reasoning = extract_think(raw)
                    return GenerationResult(
                        generation_index=request.generation_index,
                        raw_response=raw,
                        code=extract_code(raw),
                        reasoning_native=native_reasoning,
                        reasoning_extracted=extracted_reasoning,
                        reasoning_summaries=summaries,
                        latency_ms=(time.perf_counter() - started) * 1000,
                        input_tokens=_usage_value(usage, "prompt_tokens", "input_tokens"),
                        output_tokens=_usage_value(usage, "completion_tokens", "output_tokens"),
                        total_tokens=_usage_value(usage, "total_tokens"),
                        reasoning_tokens=_reasoning_token_count(usage),
                        status="ok",
                        attempts=attempt,
                        metadata=request.metadata,
                    )
                except Exception as exc:  # partial failures are data, not cancellation
                    last_error = exc
                    if attempt <= self.retries:
                        await asyncio.sleep(min(2 ** (attempt - 1), 8) + random.random() * 0.1)
            return GenerationResult(
                generation_index=request.generation_index,
                latency_ms=(time.perf_counter() - started) * 1000,
                status="error",
                error=f"{type(last_error).__name__}: {last_error}",
                attempts=self.retries + 1,
                metadata=request.metadata,
            )

    async def generate_many(
        self,
        requests: Iterable[GenerationInput],
        *,
        progress_callback: Callable[[int, int, GenerationResult], None] | None = None,
    ) -> list[GenerationResult]:
        request_list = list(requests)

        async def indexed(index: int, request: GenerationInput) -> tuple[int, GenerationResult]:
            return index, await self.generate(request)

        ordered: list[GenerationResult | None] = [None] * len(request_list)
        completed = 0
        for offset in range(0, len(request_list), self.concurrency):
            batch = request_list[offset : offset + self.concurrency]
            tasks = [
                asyncio.create_task(indexed(offset + index, request))
                for index, request in enumerate(batch)
            ]
            for task in asyncio.as_completed(tasks):
                index, result = await task
                ordered[index] = result
                completed += 1
                if progress_callback is not None:
                    progress_callback(completed, len(request_list), result)
        return [result for result in ordered if result is not None]
