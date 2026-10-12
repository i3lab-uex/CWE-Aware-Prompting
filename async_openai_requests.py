"""Backward-compatible 30-request wrapper around the experiment generator."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any, Sequence

from cwe_experiment.generation import GenerationInput, OpenAIGenerator


MODEL = "unsloth/Qwen3-0.6B-GGUF:UD-Q4_K_XL"
REQUEST_COUNT = 30
DEFAULT_BASE_URL = "http://localhost:8000/v1"


async def send_requests(
    prompt: str,
    *,
    concurrency: int = REQUEST_COUNT,
    max_tokens: int = 256,
    client: Any | None = None,
    model: str = MODEL,
    base_url: str = DEFAULT_BASE_URL,
) -> list[dict[str, Any]]:
    """Send 30 Chat Completions requests with bounded concurrency.

    The wrapper retains the prior result shape while delegating all extraction
    and partial-error handling to the experiment generator.
    """

    generator = OpenAIGenerator(
        model=model,
        base_url=base_url,
        concurrency=concurrency,
        max_tokens=max_tokens,
        retries=0,
        client=client,
    )
    results = await generator.generate_many(
        GenerationInput(prompt=prompt, generation_index=index)
        for index in range(REQUEST_COUNT)
    )
    return [
        {
            "request_id": result.generation_index + 1,
            "content": result.raw_response,
            "reasoning": result.reasoning_native or result.reasoning_extracted,
            "error": result.error,
        }
        for result in results
    ]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--concurrency", type=int, default=REQUEST_COUNT)
    parser.add_argument("--max-tokens", type=int, default=256)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY no está definida")
    result = asyncio.run(
        send_requests(
            args.prompt,
            concurrency=args.concurrency,
            max_tokens=args.max_tokens,
            model=args.model,
            base_url=args.base_url,
        )
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
