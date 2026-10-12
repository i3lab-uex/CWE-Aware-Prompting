import json

# Safe formats that are allowed for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize `content` according to the specified `format_type`.

    Parameters
    ----------
    content : bytes
        Serialized data received from an external or untrusted source.
    format_type : str
        The format of the serialized data. Supported values are those in
        ``SAFE_FORMATS`` (currently only 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in ``SAFE_FORMATS`` or if the content cannot
        be decoded properly.
    """
    # Ensure we only accept known safe formats
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Decode the bytes to a string (JSON expects text)
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Content could not be decoded as UTF-8") from exc

    # Use json.loads which is safe for basic data types
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc