import json
from typing import Any

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json",
}

def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to deserialize.
    stream_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS or if deserialization fails.
    """
    # Normalise the format string to lower case for comparison.
    fmt = stream_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    # For JSON, decode the bytes to a string and parse it.
    if fmt == "json":
        try:
            text = stream.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    # This branch is unreachable because we only support json, but kept for clarity.
    raise ValueError(f"Unhandled format: {stream_format}")