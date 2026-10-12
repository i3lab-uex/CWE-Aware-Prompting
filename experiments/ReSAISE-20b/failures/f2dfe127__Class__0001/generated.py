import json
from typing import Any

# Trusted serialization formats
_TRUSTED_FORMATS = {"json"}

def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize data from raw bytes into a Python object.

    Parameters
    ----------
    data_bytes : bytes
        Serialized data in byte form.
    format_name : str
        Name of the serialization format. Supported formats are defined in
        `_TRUSTED_FORMATS`. Currently only 'json' is allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in `_TRUSTED_FORMATS` or if decoding/parsing fails.
    """
    # Ensure the format is explicitly allowed
    if format_name.lower() not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_name!r}")

    try:
        if format_name.lower() == "json":
            # Decode bytes to string using UTF-8 (standard for JSON)
            text = data_bytes.decode("utf-8")
            # Safely parse the JSON string
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc

    # This point should never be reached because we only support 'json'.
    raise ValueError("Unhandled serialization format")