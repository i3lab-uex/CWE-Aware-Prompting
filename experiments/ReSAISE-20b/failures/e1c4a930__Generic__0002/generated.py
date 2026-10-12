import json
from typing import Any

# msgpack is optional; install with `pip install msgpack` if needed
try:
    import msgpack  # type: ignore
except ImportError:  # pragma: no cover
    msgpack = None


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, supported formats.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream to deserialize.
    data_format_type : str
        Identifier of the serialization format (e.g., 'json', 'msgpack').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported, insecure, or deserialization fails.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise ValueError("Input must be bytes-like")

    fmt = data_format_type.lower()

    if fmt == "json":
        try:
            # JSON expects text, so decode using UTF-8
            return json.loads(serialized_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON payload") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("msgpack support not available (install 'msgpack' package)")
        try:
            # raw=False ensures byte strings are decoded to str
            return msgpack.unpackb(serialized_data, raw=False)
        except (msgpack.ExtraData, msgpack.FormatError, msgpack.StackError) as exc:
            raise ValueError("Failed to deserialize MessagePack payload") from exc

    # Add more safe formats here if needed, e.g. 'yaml' with ruamel.yaml.safe_load

    raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")