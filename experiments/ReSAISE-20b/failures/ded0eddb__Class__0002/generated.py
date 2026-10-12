import json
from typing import Any

# Whitelisted safe formats for deserialization
SAFE_FORMATS = {"json"}

def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize raw bytes into a Python object.

    Parameters
    ----------
    bytes_data : bytes
        Serialized representation of the data.
    data_format : str
        The serialization format used ('json', etc.).

    Returns
    -------
    Any
        Deserialized Python object.

    Raises
    ------
    ValueError
        If the data_format is not in SAFE_FORMATS or if deserialization fails.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: '{data_format}'")

    try:
        if fmt == "json":
            # JSON expects a string; decode bytes safely
            text = bytes_data.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc

    # Should never reach here because all formats are handled above
    raise ValueError(f"Unhandled data format: '{data_format}'")