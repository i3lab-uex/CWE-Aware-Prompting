import json

# List of formats considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize `content` according to the specified `format_type`.

    Parameters
    ----------
    content : bytes
        Serialized data received from an external or untrusted source.
    format_type : str
        The format of the serialized data. Only formats listed in SAFE_FORMATS
        are allowed.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported, insecure, or if deserialization fails.
    """
    # Normalize format type to lowercase for comparison
    fmt = format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    try:
        if fmt == "json":
            # JSON expects text, so decode the bytes first
            return json.loads(content.decode("utf-8"))
    except Exception as exc:
        # Wrap any deserialization exception in a ValueError
        raise ValueError(f"Failed to deserialize content: {exc}") from exc

    # In theory unreachable because all safe formats are handled above
    raise ValueError(f"Unhandled format: {format_type}")