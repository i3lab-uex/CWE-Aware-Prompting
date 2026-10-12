import json
from html import unescape
from typing import Any

def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        Serialized data that needs to be deserialized.
    data_format : str
        The serialization format. Supported values are:
            - 'json'  : JSON format (safe).
            - 'html'  : HTML-escaped text. The function will unescape it and return a string.
            - 'text'  : Plain UTF-8 text. The function will decode and return a string.

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
        raise TypeError("data must be of type 'bytes'")

    fmt = data_format.lower()

    if fmt == "json":
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "html":
        # For HTML, we simply unescape the content and return a string.
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for HTML format") from exc
        return unescape(text)

    elif fmt == "text":
        # Plain text: just decode to string.
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for text format") from exc

    else:
        # Unsupported or potentially insecure formats (e.g., pickle, marshal) are rejected.
        raise ValueError(f"Unsupported or insecure data format: '{data_format}'")