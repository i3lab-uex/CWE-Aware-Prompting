import json
from html.parser import HTMLParser
from typing import Any, Dict, List


class SafeHTMLParser(HTMLParser):
    """
    A minimal HTML parser that extracts only the tag names and attributes
    into a nested dictionary/list structure. This avoids executing any
    embedded scripts or JavaScript.
    """

    def __init__(self):
        super().__init__()
        self.stack: List[Dict[str, Any]] = []
        self.root: Dict[str, Any] = {"type": "root", "children": []}
        self.current: Dict[str, Any] = self.root

    def handle_starttag(self, tag, attrs):
        node: Dict[str, Any] = {"type": "element", "tag": tag, "attrs": dict(attrs), "children": []}
        self.current["children"].append(node)
        self.stack.append(self.current)
        self.current = node

    def handle_endtag(self, tag):
        if self.stack:
            self.current = self.stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.current["children"].append({"type": "text", "data": text})


def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize the given byte stream into a Python object using only
    supported and safe formats.

    Parameters:
        serialized_data (bytes): The data to deserialize.
        stream_format (str): One of the supported formats ('json', 'html').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or insecure.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    fmt = stream_format.lower()
    text = serialized_data.decode("utf-8", errors="strict")

    if fmt == "json":
        # json.loads is safe for basic data types
        return json.loads(text)

    if fmt == "html":
        parser = SafeHTMLParser()
        parser.feed(text)
        return parser.root

    raise ValueError(f"Unsupported or insecure format: {stream_format}")