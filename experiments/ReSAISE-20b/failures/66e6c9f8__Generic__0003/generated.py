import json
from typing import Any

def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Only the 'json' format is supported for security reasons.  Any other
    format will raise a ValueError.

    Parameters
    ----------
    stream : bytes
        Serialized data.
    stream_format : str
        The format of the serialized data (case‑insensitive).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `stream_format` is not supported or considered insecure.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be bytes or bytearray")

    fmt = stream_format.lower().strip()
    if fmt == "json":
        try:
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc
    else:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")