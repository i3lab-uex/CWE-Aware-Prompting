import json
from typing import Any

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted formats.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of supported safe formats,
        or if deserialization fails.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    try:
        if format_type == "json":
            # JSON data is text; decode bytes to string before parsing
            text = content.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize content: {exc}") from exc

    # This point should never be reached because we guard against unsupported formats
    raise ValueError(f"Unhandled format: {format_type!r}")