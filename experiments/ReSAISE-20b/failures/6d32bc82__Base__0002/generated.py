import json

# List of serialization formats that are considered safe for deserialization.
ALLOWED_FORMATS = {
    "json": json.loads,
}

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        Identifier of the format (e.g., "json").

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or considered unsafe.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: {serialization_format!r}")

    # For JSON, the stream must be UTF‑8 encoded text.
    if fmt == "json":
        try:
            decoded = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc

        # Use json.loads to safely parse the string.
        return ALLOWED_FORMATS[fmt](decoded)

    # If additional formats are added in the future, they should be handled here.
    raise ValueError(f"Deserialization logic for {serialization_format!r} not implemented.")