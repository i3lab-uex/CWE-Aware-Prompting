import json
from typing import Any


def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object only for supported,
    safe formats.

    Supported formats
    -----------------
    - 'json' : Standard JSON deserialization using the json module.

    Parameters
    ----------
    byte_stream : bytes
        The raw serialized data.
    data_format : str
        Identifier of the serialization format. Case‑insensitive.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure, or if decoding fails.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt != "json":
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    try:
        # Decode bytes to string using UTF‑8.  If decoding fails, raise ValueError.
        text = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Byte stream is not valid UTF‑8: {exc}") from exc

    try:
        # Use the safe built‑in json loader.
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON data: {exc}") from exc