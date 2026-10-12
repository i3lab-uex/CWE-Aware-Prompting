import json
from typing import Any

# List of formats considered safe for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream that comes from an untrusted source.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The serialization format, e.g. 'json'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported, insecure or if deserialization fails.
    """
    # Ensure we only handle known safe formats
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type!r}")

    # Only JSON is supported in this implementation
    if fmt == "json":
        try:
            text = content.decode("utf-8")
        except (UnicodeDecodeError, AttributeError) as exc:
            raise ValueError("Content must be UTF‑8 encoded bytes") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # In case additional safe formats are added in the future
    raise ValueError(f"Unhandled format: {format_type!r}")