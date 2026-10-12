import asyncio
from types import SimpleNamespace
from typing import Any

from cwe_experiment.generation import GenerationInput, OpenAIGenerator, extract_code


class FakeChat:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.active = 0
        self.maximum = 0

    async def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        index = len(self.calls)
        self.active += 1
        self.maximum = max(self.maximum, self.active)
        await asyncio.sleep(0.005)
        self.active -= 1
        if index == 2:
            raise RuntimeError("partial failure")
        message = SimpleNamespace(
            content="<think>hidden</think>\n```python\ndef answer():\n    return 42\n```",
            reasoning_content="native",
        )
        usage = SimpleNamespace(prompt_tokens=3, completion_tokens=4, total_tokens=7)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=usage)


class FakeResponses:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        summary = SimpleNamespace(type="summary_text", text="short summary")
        reasoning = SimpleNamespace(type="reasoning", summary=[summary])
        message = SimpleNamespace(
            type="message",
            content=[SimpleNamespace(type="output_text", text="def result():\n    return 1")],
        )
        return SimpleNamespace(
            output_text="def result():\n    return 1",
            output=[reasoning, message],
            usage=SimpleNamespace(input_tokens=5, output_tokens=6, total_tokens=11),
        )


class UnevenChat:
    def __init__(self, batch_size: int) -> None:
        self.batch_size = batch_size
        self.calls = 0
        self.first_call_finished = False
        self.started_next_batch_too_early = False

    async def create(self, **_: Any) -> SimpleNamespace:
        self.calls += 1
        call_number = self.calls
        if call_number > self.batch_size and not self.first_call_finished:
            self.started_next_batch_too_early = True
        if call_number == 1:
            await asyncio.sleep(0.02)
            self.first_call_finished = True
        else:
            await asyncio.sleep(0)
        message = SimpleNamespace(content=f"response {call_number}")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def test_chat_adapter_bounds_concurrency_and_keeps_partial_errors() -> None:
    chat = FakeChat()
    client = SimpleNamespace(chat=SimpleNamespace(completions=chat))
    generator = OpenAIGenerator(
        model="fake",
        base_url="http://fake",
        concurrency=2,
        retries=0,
        reasoning_effort="high",
        client=client,
    )
    results = asyncio.run(
        generator.generate_many(
            GenerationInput("prompt", index) for index in range(4)
        )
    )

    assert chat.maximum == 2
    assert sum(result.status == "ok" for result in results) == 3
    assert sum(result.status == "error" for result in results) == 1
    successful = next(result for result in results if result.status == "ok")
    assert successful.code == "def answer():\n    return 42"
    assert successful.reasoning_native == "native"
    assert successful.reasoning_extracted == "hidden"
    assert successful.total_tokens == 7
    assert all(call["reasoning_effort"] == "high" for call in chat.calls)
    assert all("max_tokens" not in call for call in chat.calls)


def test_generate_many_waits_for_a_complete_batch_before_starting_next() -> None:
    chat = UnevenChat(batch_size=3)
    client = SimpleNamespace(chat=SimpleNamespace(completions=chat))
    generator = OpenAIGenerator(
        model="fake",
        base_url="http://fake",
        concurrency=3,
        retries=0,
        client=client,
    )

    results = asyncio.run(
        generator.generate_many(GenerationInput("prompt", index) for index in range(5))
    )

    assert len(results) == 5
    assert chat.calls == 5
    assert chat.started_next_batch_too_early is False


def test_responses_adapter_keeps_typed_summaries() -> None:
    responses = FakeResponses()
    client = SimpleNamespace(responses=responses)
    generator = OpenAIGenerator(
        model="fake",
        base_url="http://fake",
        api="responses",
        retries=0,
        reasoning_effort="off",
        client=client,
    )

    result = asyncio.run(generator.generate(GenerationInput("prompt", 0)))

    assert result.code == "def result():\n    return 1"
    assert result.reasoning_summaries == [
        {"type": "summary_text", "text": "short summary"}
    ]
    assert result.input_tokens == 5
    assert responses.calls[0]["reasoning"] == {"effort": "off"}
    assert "max_output_tokens" not in responses.calls[0]


def test_optional_token_limits_are_forwarded_when_explicit() -> None:
    chat = FakeChat()
    chat_client = SimpleNamespace(chat=SimpleNamespace(completions=chat))
    chat_generator = OpenAIGenerator(
        model="fake",
        base_url="http://fake",
        max_tokens=4096,
        retries=0,
        client=chat_client,
    )
    asyncio.run(chat_generator.generate(GenerationInput("prompt", 0)))

    responses = FakeResponses()
    responses_generator = OpenAIGenerator(
        model="fake",
        base_url="http://fake",
        api="responses",
        max_tokens=4096,
        retries=0,
        client=SimpleNamespace(responses=responses),
    )
    asyncio.run(responses_generator.generate(GenerationInput("prompt", 0)))

    assert chat.calls[0]["max_tokens"] == 4096
    assert responses.calls[0]["max_output_tokens"] == 4096


def test_reasoning_rejects_unknown_setting() -> None:
    client = SimpleNamespace(chat=SimpleNamespace(completions=FakeChat()))

    try:
        OpenAIGenerator(
            model="fake",
            base_url="http://fake",
            reasoning_effort="turbo",
            client=client,
        )
    except ValueError as exc:
        assert "turbo" in str(exc)
    else:
        raise AssertionError("An unknown reasoning setting must be rejected")


def test_extract_code_prefers_first_python_fence_and_falls_back_to_raw() -> None:
    assert extract_code("before\n```python\nx = 1\n```\n```python\nx = 2\n```") == "x = 1"
    assert extract_code("x = 3") == "x = 3"
