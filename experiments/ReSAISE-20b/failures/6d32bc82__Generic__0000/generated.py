import json
from typing import Any

try:
    import msgpack  # optional dependency for binary message packing
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, pre-approved formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        Format identifier ('json', 'msgpack').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe, or if deserialization fails.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # json.loads expects str, so decode assuming UTF-8
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("MessagePack support not available (msgpack library missing)")
        try:
            return msgpack.unpackb(stream, raw=False)
        except Exception as exc:  # msgpack can raise various errors
            raise ValueError("Failed to deserialize MessagePack data") from exc

    # All other formats are explicitly disallowed
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")