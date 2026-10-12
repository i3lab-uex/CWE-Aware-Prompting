import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object while restricting to safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to deserialize.
    stream_format : str
        Format specifier: currently only 'json' is supported.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Only allow json as a safe, built‑in format
    allowed_formats = {"json"}

    if stream_format.lower() not in allowed_formats:
        raise ValueError(
            f"Unsupported or insecure format: '{stream_format}'. "
            "Only 'json' is allowed."
        )

    try:
        # Decode bytes to string using UTF‑8 (common for JSON)
        text = serialized_data.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON data: {exc}") from exc