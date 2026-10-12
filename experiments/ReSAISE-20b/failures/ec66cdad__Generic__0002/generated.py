import json
from typing import Any

try:
    import msgpack  # optional dependency for binary packing
except ImportError:  # pragma: no cover
    msgpack = None


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object for a safe, known format.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    serialization_type : str
        One of the supported formats: 'json', 'msgpack'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if a required dependency is missing.
    """
    fmt = serialization_type.lower()

    if fmt == "json":
        # json.loads expects a string, so decode using UTF-8
        try:
            return json.loads(byte_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON: {exc}") from exc

    if fmt == "msgpack":
        if msgpack is None:  # pragma: no cover
            raise ValueError("msgpack support not available; install 'msgpack' package")
        try:
            # raw=False ensures binary strings are decoded to Unicode
            return msgpack.unpackb(byte_data, raw=False)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to decode msgpack data: {exc}") from exc

    # Unsupported format
    raise ValueError(f"Unsupported serialization type: {serialization_type!r}")