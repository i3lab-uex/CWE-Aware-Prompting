import json
from typing import Any

# Optional: If you want to support MessagePack safely.
try:
    import msgpack
except ImportError:  # pragma: no cover
    msgpack = None

# List of allowed, safe serialization formats.
ALLOWED_FORMATS = {
    "json": _deserialize_json,
    # "msgpack": _deserialize_msgpack,  # Uncomment if msgpack is available.
}


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        Format of the serialized data. Only formats listed in ALLOWED_FORMATS are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization format is unsupported or unsafe.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be bytes-like")

    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{serialization_format}'. "
            f"Allowed formats are: {', '.join(ALLOWED_FORMATS.keys())}"
        )

    # Delegate to the specific deserializer.
    return ALLOWED_FORMATS[fmt](stream)


# --------------------------------------------------------------------------- #
# Deserialization helpers
# --------------------------------------------------------------------------- #

def _deserialize_json(stream: bytes) -> Any:
    """
    Safely deserialize JSON data.

    JSON is safe because it maps to basic Python types (dict, list, str, int, float, bool, None).
    """
    try:
        # Decode bytes to string assuming UTF-8; ignore errors to avoid crashes.
        text = stream.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Failed to decode JSON stream as UTF-8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc


def _deserialize_msgpack(stream: bytes) -> Any:
    """
    Safely deserialize MessagePack data.

    Requires the 'msgpack' library to be installed. Uses strict type mapping.
    """
    if msgpack is None:  # pragma: no cover
        raise RuntimeError("msgpack library not available")

    try:
        # Use strict_map_key to avoid dict key type issues.
        return msgpack.unpackb(stream, raw=False, strict_map_key=True)
    except Exception as exc:
        raise ValueError("Invalid MessagePack data") from exc


# Register the msgpack deserializer only if the library is present.
if msgpack is not None:
    ALLOWED_FORMATS["msgpack"] = _deserialize_msgpack