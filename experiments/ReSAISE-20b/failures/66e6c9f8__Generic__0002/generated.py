import json
from typing import Any

# msgpack is optional; if not installed, we simply don't support it
try:
    import msgpack  # type: ignore
    _HAS_MSGPACK = True
except ImportError:
    _HAS_MSGPACK = False

# Safe formats that are allowed for deserialization
_SAFE_FORMATS = {
    "json",
    "msgpack" if _HAS_MSGPACK else None,
}

# Remove None entries that might have been added when msgpack is missing
_SAFE_FORMATS = {f for f in _SAFE_FORMATS if f}


def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object for supported, secure formats.

    Parameters
    ----------
    stream : bytes
        The serialized data as a byte string.
    stream_format : str
        Format identifier (e.g., 'json', 'msgpack').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the list of safe formats.
    TypeError
        If `stream` is not a bytes-like object.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be a bytes-like object")

    fmt = stream_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    if fmt == "json":
        # json.loads expects a str; decode using utf-8
        try:
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON stream is not valid UTF-8") from exc
        return json.loads(text)

    if fmt == "msgpack":
        # msgpack.unpackb handles bytes directly
        return msgpack.unpackb(stream, raw=False)

    # The code path should never reach here due to the earlier check
    raise ValueError(f"Unhandled format: {stream_format!r}")