import json
from typing import Any

def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object only for explicitly allowed formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        Format identifier, e.g., 'json'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered insecure.
    """
    # Normalize the format string for case‑insensitive comparison
    fmt = data_format.strip().lower()

    # Define the whitelist of safe formats
    _SAFE_FORMATS = {
        'json': json.loads,
        # Future extensions can be added here, e.g., 'msgpack': msgpack.unpackb
    }

    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: {data_format!r}")

    # Decode bytes to string using UTF-8 (common for text formats)
    try:
        decoded = byte_stream.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream is not valid UTF‑8 text") from exc

    # Perform the deserialization
    loader = _SAFE_FORMATS[fmt]
    try:
        return loader(decoded)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data as {data_format}") from exc