import json
from typing import Any

# Optional: support for msgpack if installed.
try:
    import msgpack  # type: ignore
except ImportError:
    msgpack = None


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, supported formats.

    Parameters
    ----------
    stream : bytes
        The serialized data to deserialize.
    serialization_format : str
        One of the supported formats: 'json', 'msgpack'.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `serialization_format` is not in the list of supported formats or if
        required dependencies for a format are missing.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        # JSON is text-based; decode bytes to str first.
        try:
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack support not available. Install the 'msgpack' package.")
        try:
            # Allow Python 3 compatibility and raw bytes handling.
            return msgpack.unpackb(stream, strict_map_key=False)
        except Exception as exc:
            raise ValueError("Failed to deserialize msgpack data.") from exc

    # If we reach here, the format is unsupported.
    raise ValueError(f"Unsupported serialization format: {serialization_format!r}")