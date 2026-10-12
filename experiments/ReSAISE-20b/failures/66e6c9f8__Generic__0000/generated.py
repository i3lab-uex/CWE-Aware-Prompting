import json
from typing import Any


def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        The format of the serialized data. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json"}

    fmt = stream_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    if fmt == "json":
        # Decode bytes to string before parsing
        try:
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Stream is not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc