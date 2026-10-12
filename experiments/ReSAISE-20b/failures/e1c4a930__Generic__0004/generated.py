import json
from typing import Any

try:
    import msgpack  # optional dependency for MessagePack support
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object for only supported, safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The serialized byte stream.
    data_format_type : str
        Format identifier (e.g., 'json', 'msgpack').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure, or if a required dependency is missing.
    """
    # Define safe formats
    _SAFE_FORMATS = {"json", "msgpack"}

    fmt = data_format_type.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format_type}")

    if fmt == "json":
        # JSON is text-based; decode bytes to str before parsing
        try:
            decoded = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON format") from exc
        return json.loads(decoded)

    if fmt == "msgpack":
        if msgpack is None:  # pragma: no cover
            raise ValueError("msgpack module not installed")
        return msgpack.unpackb(serialized_data, raw=False)

    # This point should never be reached due to the check above
    raise ValueError(f"Unhandled format: {data_format_type}")