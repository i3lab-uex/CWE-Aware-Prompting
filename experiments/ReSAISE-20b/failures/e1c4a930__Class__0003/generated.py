import json
from typing import Any

# Optional: msgpack can be used if available, but is considered safe for binary data.
try:
    import msgpack  # type: ignore
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object, supporting only safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format of the serialized data. Supported values are:
            - 'json'
            - 'msgpack' (if msgpack is installed)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    fmt = data_format_type.lower()

    if fmt == "json":
        try:
            # json.loads expects a str, so decode the bytes first.
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON format") from exc
        return json.loads(text)

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("MessagePack support not available (msgpack module missing)")
        try:
            # msgpack.unpackb returns bytes for binary values by default; we set raw=False
            return msgpack.unpackb(serialized_data, raw=False)
        except Exception as exc:
            raise ValueError("Failed to unpack MessagePack data") from exc

    # If we reach here, the format is unsupported.
    raise ValueError(f"Unsupported or insecure data format: {data_format_type}")