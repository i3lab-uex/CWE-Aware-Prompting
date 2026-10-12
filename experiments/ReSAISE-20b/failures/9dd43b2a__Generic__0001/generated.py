import json
from typing import Any

# Define the formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "msgpack"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object for trusted formats.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json', 'msgpack').

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    TypeError
        If `content` is not a bytes instance.
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(content, bytes):
        raise TypeError("content must be a bytes instance")

    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    if fmt == "json":
        try:
            decoded = content.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "msgpack":
        try:
            import msgpack  # Imported lazily to avoid unnecessary dependency
            return msgpack.unpackb(content, raw=False)
        except Exception as exc:
            raise ValueError("Failed to decode msgpack data") from exc

    # Should never reach here due to the SAFE_FORMATS check
    raise ValueError(f"Unhandled format: {format_type!r}")