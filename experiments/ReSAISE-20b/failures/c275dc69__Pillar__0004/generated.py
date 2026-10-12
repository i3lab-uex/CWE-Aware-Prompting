import json
from html.parser import HTMLParser
from typing import Any


class _SafeHTMLParser(HTMLParser):
    """
    A minimal HTML parser that only extracts data from safe tags.
    It discards all markup and returns the concatenated text content.
    """
    def __init__(self):
        super().__init__()
        self.text_parts = []

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)

    def get_text(self) -> str:
        return "".join(self.text_parts)


def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    predefined safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        One of the supported formats: 'json', 'html'.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Ensure we work with a string for text-based formats
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    fmt = stream_format.lower()

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "html":
        parser = _SafeHTMLParser()
        parser.feed(text)
        return parser.get_text()

    # Any other format is disallowed
    raise ValueError(f"Unsupported or insecure format: {stream_format}")