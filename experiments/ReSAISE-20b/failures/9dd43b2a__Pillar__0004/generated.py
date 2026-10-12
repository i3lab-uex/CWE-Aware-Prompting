import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
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
    object
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of supported and safe formats.
    """
    # Normalise format type
    fmt = format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # For JSON, the content is expected to be UTF‑8 encoded
    try:
        decoded = content.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Content must be UTF‑8 encoded JSON") from exc

    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Invalid JSON data") from exc