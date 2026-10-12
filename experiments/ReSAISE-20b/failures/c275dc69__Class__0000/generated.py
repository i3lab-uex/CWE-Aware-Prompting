import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe,
    predefined formats. Currently supports JSON only.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        Identifier of the format. Supported values are:
            'json'  - JSON data.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If `stream_format` is unsupported or if the data cannot be parsed.
    """
    # Ensure that only allowed formats are used
    allowed_formats = {"json"}
    if stream_format.lower() not in allowed_formats:
        raise ValueError(f"Unsupported or insecure format: {stream_format!r}")

    # Decode bytes to text (JSON is text-based)
    try:
        decoded = serialized_data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Serialized data is not valid UTF-8") from exc

    # Parse JSON safely
    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Failed to decode JSON data") from exc