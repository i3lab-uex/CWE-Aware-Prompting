import json

# Define the whitelist of safe serialization formats.
ALLOWED_FORMATS = {"json"}

def deserialize_data(raw_data: bytes, serialization_format: str):
    """
    Safely deserialize raw bytes into a Python object based on the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of an object.
    serialization_format : str
        Identifier for the serialization format ('json', etc.).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    # Normalise the format string to avoid accidental case variations.
    fmt = serialization_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{serialization_format}'. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}."
        )

    # For JSON, decode bytes to str and then parse.
    try:
        if fmt == "json":
            # Ensure the data is valid UTF-8.
            text = raw_data.decode("utf-8")
            return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc