import json
from typing import Any

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize `content` according to the specified `format_type`.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        Format of the serialized data. Only formats listed in `SAFE_FORMATS`
        are accepted.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure, or if deserialization fails.
    """
    # Normalize format_type to lowercase for comparison
    fmt = format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    try:
        if fmt == "json":
            # JSON is text based; ensure the bytes are decoded as UTF‑8
            return json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize {format_type!r}: {exc}") from exc

    # This point should never be reached because all safe formats are handled
    raise ValueError(f"Unhandled safe format: {format_type!r}")