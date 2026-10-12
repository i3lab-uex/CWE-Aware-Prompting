import json
from html.parser import HTMLParser
from typing import Any


class _SafeHTMLParser(HTMLParser):
    """
    A minimal HTML parser that extracts text data only.
    This is used to safely deserialize simple string-based
    representations encoded as HTML (e.g., escaped text).
    """

    def __init__(self):
        super().__init__()
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        self._text_parts.append(data)

    def get_text(self) -> str:
        return "".join(self._text_parts)


def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object based on the given format.

    Parameters
    ----------
    data : bytes
        The serialized data to deserialize.
    data_format : str
        The format of the serialized data. Supported formats are:
            - 'json'  : JSON encoded data.
            - 'html'  : Plain text escaped in HTML (safe subset).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be of type 'bytes'")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            # decode bytes to str assuming UTF-8, the most common encoding for JSON
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "html":
        try:
            text = data.decode("utf-8")
            parser = _SafeHTMLParser()
            parser.feed(text)
            # return the raw text; if you need a specific type, adapt here
            return parser.get_text()
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid HTML data") from exc

    # Unsupported or insecure format
    raise ValueError(f"Unsupported or insecure data format: {data_format}")