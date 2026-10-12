import json
from html.parser import HTMLParser
from typing import Any, Union


class _SimpleHTMLToDictParser(HTMLParser):
    """
    Very small and safe parser that converts an HTML snippet into a nested dictionary.
    This is *not* intended to fully parse arbitrary HTML; it only extracts tags, attributes
    and text content in a deterministic way. It is deliberately limited to avoid executing
    scripts or other unsafe operations.
    """
    def __init__(self):
        super().__init__()
        self.stack: list[dict] = []
        self.root: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Union[str, None]]]) -> None:
        element = {"tag": tag}
        if attrs:
            element["attrs"] = dict(attrs)
        self.stack.append(element)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        element = self.stack.pop()
        # Attach to parent or set as root if no parent exists
        if self.stack:
            parent = self.stack[-1]
            children = parent.setdefault("children", [])
            children.append(element)
        else:
            self.root = element

    def handle_data(self, data: str) -> None:
        if not self.stack:
            return
        current = self.stack[-1]
        text = data.strip()
        if text:
            children = current.setdefault("children", [])
            children.append({"text": text})

    def get_result(self) -> dict | None:
        return self.root


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize `input_data` based on the provided `input_format`.

    Supported formats (case‑insensitive):
        - 'json': JSON data decoded into Python objects.
        - 'html': Very small, safe HTML snippet parsed into a nested dictionary structure.

    Raises:
        ValueError: If the format is unsupported or considered insecure.
    """
    if not isinstance(input_data, bytes):
        raise TypeError("input_data must be of type 'bytes'")

    fmt = input_format.strip().lower()
    if fmt == "json":
        try:
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "html":
        try:
            parser = _SimpleHTMLToDictParser()
            parser.feed(input_data.decode("utf-8"))
            result = parser.get_result()
            if result is None:
                raise ValueError("Empty or malformed HTML")
            return result
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 in HTML data") from exc

    # Any other format is disallowed
    raise ValueError(f"Unsupported or insecure input_format: {input_format!r}")