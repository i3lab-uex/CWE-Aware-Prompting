import json
from typing import Any

try:
    import msgpack  # optional dependency for binary serialization
except ImportError:  # pragma: no cover
    msgpack = None


def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Only the following formats are considered safe:
        - 'json'   : UTF‑8 encoded JSON.
        - 'msgpack': MessagePack (binary) with raw strings decoded to text.

    Parameters
    ----------
    data : bytes
        The serialized stream of data.
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
    fmt = data_format.lower()
    if fmt == "json":
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "msgpack":
        if msgpack is None:  # pragma: no cover
            raise ValueError("msgpack support not available")
        try:
            return msgpack.unpackb(data, raw=False)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid MessagePack data") from exc

    raise ValueError(f"Unsupported or unsafe format: {data_format}")