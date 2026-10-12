import json
from html import unescape
from typing import Any


def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to be deserialized.
    stream_format : str
        The format of the serialized data. Supported values are:
            - 'json'   : JSON encoded bytes.
            - 'html'   : HTML escaped string that should be unescaped.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If an unsupported or insecure format is requested, or if the data cannot be parsed.
    """
    # Normalise the format string
    fmt = stream_format.strip().lower()

    if fmt == "json":
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF-8 encoded") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "html":
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("HTML data must be UTF-8 encoded") from exc

        # For safety we only unescape; no other processing is performed.
        return unescape(text)

    else:
        # Any other format would require a potentially unsafe deserializer
        raise ValueError(f"Unsupported or insecure stream format: {stream_format}")