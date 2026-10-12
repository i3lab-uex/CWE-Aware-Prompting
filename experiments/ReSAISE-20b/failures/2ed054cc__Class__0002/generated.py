import json

# Allowed serialization formats for safe deserialization.
ALLOWED_FORMATS = {"json"}

def deserialize_data(raw_data: bytes, serialization_format: str):
    """
    Safely deserializes raw serialized data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The raw serialized data.
    serialization_format : str
        The format used for serialization (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    # Normalize and validate the requested format
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    # Only JSON is supported in this secure implementation
    if fmt == "json":
        try:
            # Decode bytes to text using UTF-8
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode JSON data: invalid UTF-8") from exc

        try:
            # Parse JSON into a Python object
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # In practice, other formats would be added here with secure parsers.