import json
from typing import Any

try:
    import msgpack  # optional dependency; safe for binary data
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, approved formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        One of the allowed formats: 'json', 'msgpack'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if not isinstance(stream, bytes):
        raise TypeError("stream must be of type 'bytes'")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # JSON is text; decode using UTF-8
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack library not installed")
        try:
            return msgpack.unpackb(stream, raw=False)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to deserialize msgpack data") from exc

    # Any other format is explicitly disallowed
    raise ValueError(f"Unsupported serialization format: {serialization_format}")