import json
from typing import Any

# Only the following formats are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        Raw serialized data.
    data_format : str
        The format used for serialization. Supported values are defined in
        ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    try:
        if fmt == "json":
            # JSON data is expected to be UTF‑8 encoded.
            text = bytes_data.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc