import json
from html.parser import HTMLParser
from typing import Any

class SafeHTMLParser(HTMLParser):
    """
    A minimal HTML parser that extracts text data while ignoring tags.
    This can be used to safely convert simple HTML snippets into plain text.
    """
    def __init__(self):
        super().__init__()
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        self._text_parts.append(data)

    def get_text(self) -> str:
        return ''.join(self._text_parts)


def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialization ('json' or 'html').

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, str).

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(data, bytes):
        raise ValueError("Input data must be of type 'bytes'.")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            # Decode assuming UTF-8; raise UnicodeDecodeError if invalid
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 for JSON deserialization.") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    elif fmt == "html":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 for HTML deserialization.") from exc

        parser = SafeHTMLParser()
        parser.feed(text)
        return parser.get_text()

    else:
        # Reject any other formats (e.g., pickle, marshal) to avoid unsafe deserialization
        raise ValueError(f"Unsupported or insecure format '{data_format}'.")