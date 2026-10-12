import json
from typing import Any

# Optional: support for msgpack if desired and considered safe
try:
    import msgpack  # type: ignore[import]
except ImportError:
    msgpack = None


def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    approved, safe formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Format identifier, e.g. 'json', 'msgpack'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        # JSON is text-based; decode to string first
        try:
            decoded = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 for JSON") from exc
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack support not available")
        try:
            return msgpack.unpackb(data, raw=False)
        except Exception as exc:  # pylint: disable=broad-except
            raise ValueError("Invalid msgpack data") from exc

    # Add other safe formats here as needed

    raise ValueError(f"Unsupported or unsafe format: {data_format}")