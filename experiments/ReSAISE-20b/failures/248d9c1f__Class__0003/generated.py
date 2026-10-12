import json
from typing import Any

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Safely deserialize data from raw bytes into a Python object.

    Only the following formats are allowed:
        - 'json'

    Parameters
    ----------
    byte_data : bytes
        The serialized object in byte format.
    encoding_type : str
        The serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is not supported or if deserialization fails.
    """
    allowed_formats = {"json"}

    if encoding_type.lower() not in allowed_formats:
        raise ValueError(f"Unsupported or dangerous format: {encoding_type!r}")

    try:
        if encoding_type.lower() == "json":
            # Decode bytes to string using UTF-8 (common JSON encoding)
            text = byte_data.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Failed to deserialize data") from exc