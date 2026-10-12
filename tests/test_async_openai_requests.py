import asyncio
from types import SimpleNamespace
from typing import Any

from async_openai_requests import MODEL, REQUEST_COUNT, send_requests


class FakeCompletions:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.active = 0
        self.maximum_active = 0

    async def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        self.active += 1
        self.maximum_active = max(self.maximum_active, self.active)
        await asyncio.sleep(0)
        self.active -= 1
        message = SimpleNamespace(content=f"respuesta {len(self.calls)}")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class FakeClient:
    def __init__(self) -> None:
        self.completions = FakeCompletions()
        self.chat = SimpleNamespace(completions=self.completions)


def test_send_requests_makes_30_concurrent_calls() -> None:
    client = FakeClient()

    results = asyncio.run(send_requests("hola", max_tokens=17, client=client))

    assert len(results) == REQUEST_COUNT == 30
    assert len(client.completions.calls) == REQUEST_COUNT
    assert client.completions.maximum_active == REQUEST_COUNT
    assert [result["request_id"] for result in results] == list(
        range(1, REQUEST_COUNT + 1)
    )
    assert all(call["model"] == MODEL for call in client.completions.calls)
    assert all(call["max_tokens"] == 17 for call in client.completions.calls)
    assert all(
        call["messages"] == [{"role": "user", "content": "hola"}]
        for call in client.completions.calls
    )


def test_send_requests_bounds_concurrency() -> None:
    client = FakeClient()

    results = asyncio.run(send_requests("hola", concurrency=3, client=client))

    assert len(results) == REQUEST_COUNT
    assert len(client.completions.calls) == REQUEST_COUNT
    assert client.completions.maximum_active == 3
