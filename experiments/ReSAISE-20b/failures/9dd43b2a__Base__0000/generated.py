import json
from typing import Any

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream that comes from an untrusted source.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If the format is not in the list of trusted formats or if deserialization fails.
    """
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    try:
        if fmt == "json":
            # Ensure the input is decoded to a string before parsing.
            return json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to deserialize JSON content: {exc}") from exc

    # In practice this point is unreachable because we only allow json.
    raise ValueError(f"Unhandled format: {format_type!r}")